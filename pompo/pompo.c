#include "pompo.h"
#include "file.h"
#include "profile.h"
#include "module.h"
#include "matrix.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <omp.h>

extern int verbosity;

void onexit() {
  module_unload_all();
}

void export_json(FILE* f, struct profile* p, struct matrix* res, struct file** files, int n_files) {
  int i,j;
  fprintf(f, "{\n\"signature\":\"");
  if (p->p_prefilt) {
    fprintf(f, "%s#",p->p_prefilt->b_sign);
  }
  fprintf(f, "%s#%s#%s\",\n", 
	  p->p_seg->b_sign, 
	  p->p_dist->b_sign,
	  p->p_docdist->b_sign);
  
  fprintf(f, "\"corpus_scores\": \n[\n");
  for (i = 0; i < n_files; ++i) {
    fprintf(f, "  [");
    for (j = 0; j < n_files; ++j) {
      if (j) fprintf(f, ", ");
      fprintf(f, "%.6f", res->m_data[i][j]);
    }
    if (i < n_files - 1)fprintf(f, "],\n");
    else fprintf(f, "]\n");
  }
  fprintf(f, "],\n");
  fprintf(f, "\"filenames\":\n[");
  for (i = 0; i < n_files; ++i) {
     if (i) fprintf(f, ", ");
     fprintf(f, "\"%s\"",files[i]->f_name);
  }
  fprintf(f, "]\n}\n");
}


int main(int argc, char* argv[]) {
  struct profile prof;
  struct file **files;
  int* pairs;
  int n_files, n_pairs = 1;
  int opt;
  int all_pairs = 1;
  int i,j, ii;
  int n_th = 2;
  struct matrix* res;
  struct module *m;
  FILE* out = 0;
  char* dist_prof = strdup("cthct");

  while ((opt = getopt(argc, argv, "qv:p:P:t:o:")) != -1) {
    char *c, *tmp, *save;
    char *delims[2] = {",", ":"};
    int did = 0;
    int *p;
    switch (opt) {
    case 'q':
      verbosity = -1;
      break;
    case 'v':
      verbosity = atoi(optarg);
      break;
    case 'o':
      if ((out = fopen(optarg, "w")) == NULL) {
	perror(optarg);
	return EXIT_FAILURE;
      }
    case 't':
      n_th = atoi(optarg);
      break;
    case 'p':
      dist_prof = strdup(optarg);
      break;
    case 'P':
      all_pairs = 0;
      for (c = optarg; *c != '\0'; ++c) {
	if (*c == ':') ++n_pairs;
      }
      p = pairs = (int*) malloc(2*n_pairs*sizeof(int));
      save = tmp = strdup(optarg);
      c = strtok(tmp, delims[did]);
      while (c != NULL) {
	*p++ = atoi(c);	
	did ^=  1;
	c = strtok(NULL, delims[did]);
      }
      free(save);
      if (did) {
	return EXIT_FAILURE;
      }

      break;
    default: /* '?' */
      fprintf(stderr, "Usage: %s [-v <num>] [-q] [-o <outfile>] [-p <pairs_desc>] file1 file2 [file3 ...]\n",
	      argv[0]);
      return EXIT_FAILURE;
    }
  }    

  omp_set_num_threads(n_th);

  n_files = argc - optind;
  if (n_files < 2) {
    fprintf(stderr, "Expected at least 2 files\n");
    return EXIT_FAILURE;
  }

  
  LOG(1)  printf("opening %d files\n", n_files);
  files = (struct file**) malloc(n_files*sizeof(struct file*));
  for (i = 0, ii=0; i < n_files; ++i) {
    struct file *f;    
    if ((f = file_load(argv[optind+i])) == NULL) {
      fprintf(stderr, "skipping unreadable file %s\n", argv[optind+i]);
    } else {
      files[ii++] = f;      
    }
  }
  n_files = ii;
  LOG(1) printf("loaded %d files\n", n_files);
  
  if (all_pairs) {
    int *pair;
    n_pairs = ((n_files-1)*n_files)/2;
    pair = pairs = (int*) malloc(2*n_pairs*sizeof(int));

    for (i = 0; i < n_files; ++i) {
      for (j = i+1; j < n_files; ++j) {
	*pair++ = i;
	*pair++ = j;
      }
    }
  } 


  profile_init(&prof);

  m = module_load("segmenters/newline.so");
  module_bind(m, "1", &prof);
  m = module_load("distances/levenshtein.so"); 
  // m = module_load("distances/hamming.so"); 
  module_bind(m, NULL, &prof);
  m = module_load("prefilters/t.so");
  module_bind(m, "t", &prof);

  m = module_load("docdist/matching.so");
  module_bind(m, dist_prof, &prof);

  free(dist_prof);

  atexit(onexit);

  if (!profile_check(&prof)) {
    fprintf(stderr, "Invalid profile, check module load list\n");
    return EXIT_FAILURE;
  }

  if ((res = profile_run(&prof, files, n_files, pairs, n_pairs)) == NULL) {
    return EXIT_FAILURE;
  }
  
  if (!out && (out = fdopen(3, "w")) == NULL) {
    out = stdout;
  }
  export_json(out, &prof, res, files, n_files);

  matrix_delete(res);

  for (i = 0; i < n_files; ++i) {
    file_unload(files[i]);
  }


  free(files);
  free(pairs);

  module_unload_all();
 

  return EXIT_SUCCESS;
}
