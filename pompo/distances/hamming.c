#include <wchar.h>
#include <stdlib.h>
#include <stdio.h>
#include "profile.h"
#include "segment.h"

float hamming_distance(struct binding* this __attribute__((unused)),
		       wchar_t **seg1, wchar_t **seg2) {
  int n1, n2, mn, mx, i, diff;

  n1 = seg_len(seg1);
  n2 = seg_len(seg2);
  if (n1 < n2) {
    mx = n2;
    mn = n1;
  } else {
    mx = n1;
    mn = n2;
  }
  diff = mx - mn;
  
  for (i = 0; i < mn; ++i) {
    if ((*seg1)[i] != (*seg2)[i]) {
      ++diff;
    }
  }
   
  return (float)diff / (float) mx;
}

void module_loader(void) {
}

void module_unbinder(struct profile* p) {
  if (p->p_dist == NULL) return;
  free(p->p_dist);
  p->p_dist = NULL;
}

int module_binder(const char* args __attribute__((unused)), struct profile* p) {
  if (p->p_dist != NULL) {
    fprintf(stderr, "unable to bind module: Distance module already bound\n");
    return -1;
  }

  p->p_dist =  (struct binding*) malloc(sizeof(struct binding));
  p->p_dist->b_data = NULL;
  p->p_dist->b_sign = "D:hamming";
  p->p_dist->run = hamming_distance;
  return 0;
}
