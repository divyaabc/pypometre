#include "profile.h" 
#include "file.h"
#include "matrix.h"
#include "pompo.h"
#include <string.h>
#include <stdio.h>
#include "segment.h"

int verbosity = 0;

void profile_init(struct profile* p) {
  memset(p, 0, sizeof(struct profile));
}

int profile_check(struct profile* p) {
  if (p->p_seg == NULL) {;
    fprintf(stderr, "No suitable segmenter found\n");
    return 0;
  }

  if (p->p_dist == NULL) {;
    fprintf(stderr, "No suitable distance found.\n");
    return 0;
  }

  return 1;
}

struct textinfo* profile_run_prefilt(struct profile* p, struct file* f) {
  struct textinfo* ti;
  if (p->p_prefilt == NULL) {
    return &f->f_orig;
  }
 #pragma omp critical
  {
    ti = file_find_text(f, p->p_prefilt->b_sign);
    if (ti == NULL) {
      prefilt_t run = (prefilt_t) p->p_prefilt->run;
      ti = run(p->p_prefilt, f);
      file_add_text(f, ti);
    }
  } 
  return ti;
}

struct seginfo* profile_run_seg(struct profile* p, struct file* f, struct textinfo* ti) {
  struct seginfo* si;
  #pragma omp critical 
  {
  si = file_find_seg(f, p->p_seg->b_sign, ti);
  if (si == NULL) {
    seg_t run = (seg_t) p->p_seg->run;
    si = run(p->p_seg, f, ti);
    file_add_seg(f, si);
  }
  }
  return si;
}

struct matrix* profile_run_dist(struct profile* p, struct seginfo* seg1, struct seginfo* seg2) {
  wchar_t **s1, **s2;
  dist_t d = (dist_t) p->p_dist->run;
  struct matrix *m;
  unsigned int i, j;
  
  if (seg1->si_size > seg2->si_size) {
    struct seginfo* tmp = seg1;
    seg1 = seg2;
    seg2 = tmp;
  }

  m = matrix_init(seg1->si_size, seg2->si_size);

  for (s1 = seg1->si_segs, i=0; *(s1+1) != NULL; ++s1, ++i) {
    for (s2 = seg2->si_segs, j=0; *(s2+1) != NULL; ++s2, ++j) {
      m->m_data[i][j] = d(p->p_dist, s1, s2);
      /* wchar_t* c = *s1; */
      /* while (c != *(s1+1)) { */
      /* 	printf("%c", *c++); */
      /* } */
      /* c = *s2; */
      /* while (c != *(s2+1)) { */
      /* 	printf("%c", *c++); */
      /* } */
      /* printf("%f\n",  m->m_data[i][j]); */
    }
  }

  for (i = seg1->si_size; i < seg2->si_size; ++i) {
    for (j = 0; j < seg2->si_size; ++j) {
      m->m_data[i][j] = 1.0f;
    }
  }

  // matrix_to_png(m, "seg_dist.png");
  //exit(0);

  return m;
}

float profile_run_docdist(struct profile* p, struct matrix* m) {
  docdist_t run = p->p_docdist->run;
  float d;
  d = run(p->p_docdist, m);
  return d;
}

struct matrix* profile_run(struct profile* p, struct file** files, int nf, int* pairs, int np) {
  int pi;
  struct matrix* out;

  srand(time(NULL));

  if (p == NULL || !profile_check(p)) {
    return NULL;
  }

  out = matrix_init(nf, nf);
  for (pi = 0; pi < nf; ++pi) {
    out->m_data[pi][pi] = 0.0;
  }
  


#pragma omp parallel for schedule(dynamic, 1)
  for (pi = 0; pi < np; ++pi) {
    int i = pairs[2*pi];
    int j = pairs[2*pi+1];
    struct file *f1 = files[i];
    struct file *f2 = files[j];
    struct textinfo *t1, *t2;
    struct seginfo *s1, *s2;
    struct matrix* m;
    double d;

    {
      t1 = profile_run_prefilt(p, f1);
      s1 = profile_run_seg(p, f1, t1);
    }

    {
    t2 = profile_run_prefilt(p, f2);
    s2 = profile_run_seg(p, f2, t2);
    }  
    

    m = profile_run_dist(p, s1, s2);
    
    d = profile_run_docdist(p, m);
    out->m_data[j][i] = out->m_data[i][j] = d;
    LOG(0) printf("\r%02d/%d (%2.f%%)    docdist = %f    ",
	   pi, np, (float)pi*100.f/(float)np,d);
    fflush(stdout);

    matrix_delete(m);
  }
  LOG(0) printf("\n");
  return out;
}
