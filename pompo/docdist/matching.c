#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "profile.h"
#include "asp.h"
#include "matrix.h"

struct matching {
  long* rows;
  long* cols;
};

float energy(struct matrix* m, struct matching* s) {
  unsigned int i;
  float c = 0.0f;
  for (i = 0; i < m->m_rows; ++i) {
    c += m->m_data[i][s->rows[i]];
  }
  return c;
}

struct matching* init_matching(struct matrix* m) {
  struct matching *s;
  unsigned int i;
  s = (struct matching*) malloc(sizeof (struct matching));
  s->rows = (long*) malloc(m->m_size * sizeof(long));
  s->cols = (long*) malloc(m->m_size * sizeof(long));

  for (i = 0; i < m->m_rows; ++i) {
    s->rows[i] = s->cols[i] = i;
  }
  for (i = m->m_rows; i < m->m_cols; ++i) {
    s->cols[i] = -1;
  }
  
  return s;
}

void matching_delete(struct matching* m) {
  free(m->rows);
  free(m->cols);
}

/* void neighbor(struct matching* new, struct matching* from, struct matrix* m) { */
/*   int i, j; */
/*   memcpy(new->cols, from->cols, m->m_cols*sizeof(long)); */
/*   memcpy(new->rows, from->rows, m->m_rows*sizeof(long)); */

/*   i = rand() % m->m_rows; */
/*   do { */
/*     j = rand() % m->m_cols; */
/*   } while (j == from->rows[i]); */

/*   new->rows[i] = j; */
/*   new->cols[j] = i;   */

/*   if (from->cols[j] >= 0) { */
/*     new->rows[from->cols[j]] = from->rows[i]; */
/*   } */
/*   new->cols[from->rows[i]] = from->cols[j]; */
/* } */

float gen_swap(struct matching* from, struct matrix* m, float e, int *ii, int *jj) {
  int i,j;
  i = *ii = rand() % m->m_rows;
  do {
    j = *jj = rand() % m->m_cols;
  } while (j == from->rows[i]);

  e -= m->m_data[i][from->rows[i]];
  e += m->m_data[i][j];

  if (from->cols[j] >= 0) {
    e -= m->m_data[from->cols[j]][j];
    e += m->m_data[from->cols[j]][from->rows[i]];
  }

  return e;
}

void apply_swap(struct matching* m, int i, int j) {
  if (m->cols[j] >= 0) {
    m->rows[m->cols[j]] = m->rows[i];
  }
  m->cols[m->rows[i]] = m->cols[j];

  m->rows[i] = j;
  m->cols[j] = i;  
}

#define BIG 100000000
int metropolis(float de, float t) {
  return (float)(rand()%BIG)/(float)BIG < exp(-de/t);
}


void convolve(char** p, struct matrix* m, struct matrix* out) {
  char* end;
  long size, hsize;
  int i,j;
  int k;

  size = strtol(*p+1, &end, 10);
  if (end == *p+1) {
    size = 5;
  }
  *p = end;

  hsize = size >> 1;
  
  for (i = 0; i < m->m_rows; ++i) {
    for (j = 0; j < m->m_cols; ++j) {
      /* if (i < hsize || i >= m->m_rows-hsize || j < hsize || j >= m->m_cols-hsize) { */
      /* 	out->m_data[i][j] = m->m_data[i][j]; */
      /* } else { */
      /* 	float v = 0.f; */
      /* 	for (k = -hsize; k <= hsize; ++k) { */
      /* 	  v += m->m_data[i+k][j+k]; */
      /* 	} */
      /* 	out->m_data[i][j] = v / (float) size; */
      /* } */
      {
      	float v = 0.f;
      	for (k = -hsize; k <= hsize; ++k) {
      	  if (i+k >= 0 && i+k < m->m_size && j+k >= 0 && j+k < m->m_size) {
      	    v += m->m_data[i+k][j+k];
      	  } else {
      	    v += 1.0f;
      	  }
      	}
      	out->m_data[i][j] = v / (float) size;
      }

    }
  }
  
}

void treshold(char** p, struct matrix* m) {
  char* end;
  float t = 0.7f;
  unsigned int i, j;

  t = strtof(*p+1, &end);
  if (end == *p+1) {
    t = 0.7;    
  }
  *p = end;
  
  //matrix_to_png(m, "a.png");

  for (i = 0; i < m->m_rows; ++i) {
    for (j = 0; j <  m->m_cols; ++j) {
      if (m->m_data[i][j] > t) {
	m->m_data[i][j] = 1.f;
      } 
    }
  }

  //matrix_to_png(m, "b.png");
}

struct matching* hungarian(char** p, struct matrix* in, struct matrix* out) {
  unsigned int i;
  struct matching* match;
  match = init_matching(in);

  ++(*p);

  matrix_copy(out, in);

  asp(out->m_size, out->m_data, match->rows, match->cols);

  matrix_fill_one(out);

  for (i = 0; i < out->m_rows; ++i) {
    out->m_data[i][match->rows[i]] = in->m_data[i][match->rows[i]];
  }

  return match;
}

#define SWAP(t, a,b) {t __tmp; __tmp=(a); (a)=(b); (b)=__tmp;}

#define N 50

struct matching* annealing(char** p, struct matrix* in, struct matrix* out) {
  unsigned int i,j;
  float t = 0.0f;
  float rate = 0.5f;
  float e, enew;
  int si,sj;
  struct matching* sol = init_matching(in);
  struct matching* tmp = init_matching(in);
  
  ++(*p);

  e = energy(in, tmp);
  for (i = 0; i < N; ++i) {
    t += gen_swap(tmp, in, e, &si, &sj) - e;
    apply_swap(tmp, si, sj);
  }
  t = -fabsf(t/(float)N) / log(rate); 

  matching_delete(tmp);
  free(tmp);

  e = energy(in, sol);
  for (j = 0; j < in->m_rows; ++j) {
    for (i = 0; i < in->m_rows; ++i) {
      enew = gen_swap(sol, in, e, &si, &sj);      
      if (enew < e || metropolis(enew - e, t)) {
	e = enew;
	apply_swap(sol, si, sj);
      } 
    }
    t *= 0.9;    
  }

  matrix_fill_one(out);

  for (i = 0; i < out->m_rows; ++i) {
    out->m_data[i][sol->rows[i]] = in->m_data[i][sol->rows[i]];
  }

  return sol;
}

float matching_docdist(struct binding* self, struct matrix* segdists) {
  char* profile = (char*) self->b_data;
  struct matrix * tmp, *ptr;
  float d = 0.f;
  unsigned int i;
  struct matching* match = NULL;

  tmp = matrix_init(segdists->m_rows, segdists->m_cols);
  /* for (i = segdists->m_rows; i < segdists->m_size; ++i) { */
  /*   memcpy(tmp->m_data[i], segdists->m_data[i], segdists->m_size*sizeof(float)); */
  /* } */
  matrix_fill_one(tmp);
  ptr = tmp;

  //char f[64];

  while (*profile != '\0') {
    //sprintf(f, "filt_%s.png", profile);
   
    switch (*profile) {
    case 'c':
      convolve(&profile, segdists, tmp);
      SWAP(struct matrix*, segdists, tmp);
      break;
    case 't':
      treshold(&profile, segdists);
      break;
    case 'h':
      match = hungarian(&profile, segdists, tmp);
      SWAP(struct matrix*, segdists, tmp);
      break;
    case 'a':
      match = annealing(&profile, segdists, tmp);
      SWAP(struct matrix*, segdists, tmp);
      break;
    default:
      break;
    }

    // matrix_to_png(segdists, f);
  }

  for (i = 0; i < segdists->m_rows; ++i) {
    d += segdists->m_data[i][match->rows[i]];
  }
  d /= (float)segdists->m_rows;

  matching_delete(match);
  free(match);

  matrix_delete(ptr);

  return d;
}

void module_loader(void) {
}

void module_unbinder(struct profile* p) {
  if (p->p_docdist == NULL) return;
  free(p->p_docdist->b_data);
  free(p->p_docdist->b_sign);
  free(p->p_docdist);
  p->p_docdist = NULL;
}

int module_binder(const char* args, struct profile* p) {
  char* profile;

  if (p->p_docdist != NULL) {
    fprintf(stderr, "unable to bind module: Document distance module already bound\n");
    return -1;
  }

  if (args != NULL) {
    int h = 0;
    const char *s = args;
    while (*s != '\0') {
      if ((*s == 'a' || *s == 'h') && ++h > 1) {
        fprintf(stderr, "more than one hungarian in docdist profile\n");	
        return -1;
      }
      ++s;
    }
    if (!h) {
	  fprintf(stderr, "no hungarian in docdist profile\n");	
	  return -1;
    }
    profile = strdup(args);
  } else {
    profile = strdup("cthct");
    printf("matching: using default profile '%s'\n",  profile);
  }

  p->p_docdist = (struct binding*) malloc(sizeof(struct binding));

  p->p_docdist->b_sign = (char*) malloc((3+strlen(profile))*sizeof(char));
  sprintf(p->p_docdist->b_sign, "M:%s", profile);
  p->p_docdist->b_data = (void*) profile;
  p->p_docdist->run = matching_docdist;

  return 0;
}
