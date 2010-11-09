#include <wchar.h>
#include <stdlib.h>
#include <stdio.h>
#include "profile.h"
#include "segment.h"


size_t
lev_edit_distance(size_t len1, const wchar_t *string1,
                  size_t len2, const wchar_t *string2)
{
 /*
    The code of this function is based on David Necas's
    (yeti@physics.muni.cz) Python Levenshtein library:
    http://trific.ath.cx/python/levenshtein/
  */
  size_t i;
  size_t *row;  /* we only need to keep one row of costs */
  size_t *end;
  size_t half;

  /* strip common prefix */
  while (len1 > 0 && len2 > 0 && *string1 == *string2) {
    len1--;
    len2--;
    string1++;
    string2++;
  }

  /* strip common suffix */
  while (len1 > 0 && len2 > 0 && string1[len1-1] == string2[len2-1]) {
    len1--;
    len2--;
  }

  /* catch trivial cases */
  if (len1 == 0)
    return len2;
  if (len2 == 0)
    return len1;

  /* make the inner cycle (i.e. string2) the longer one */
  if (len1 > len2) {
    size_t nx = len1;
    const wchar_t *sx = string1;
    len1 = len2;
    len2 = nx;
    string1 = string2;
    string2 = sx;
  }
  /* check len1 == 1 separately */
  if (len1 == 1) {
      return len2 - (wmemchr(string2, *string1, len2) != NULL);
  }
  len1++;
  len2++;
  half = len1 >> 1;

  /* initalize first row */
  row = (size_t*)alloca(len2*sizeof(size_t));//(size_t*)malloc(len2*sizeof(size_t));
  if (!row)
    return (size_t)(-1);
  end = row + len2 - 1;
  for (i = 0; i < len2 - half; i++)
    row[i] = i;

  /* go through the matrix and compute the costs.  yes, this is an extremely
   * obfuscated version, but also extremely memory-conservative and relatively
   * fast.  */
  {
    /* in this case we don't have to scan two corner triangles (of size len1/2)
     * in the matrix because no best path can go throught them. note this
     * breaks when len1 == len2 == 2 so the memchr() special case above is
     * necessary */
    row[0] = len1 - half - 1;
    for (i = 1; i < len1; i++) {
      size_t *p;
      const wchar_t char1 = string1[i - 1];
      const wchar_t *char2p;
      size_t D, x;
      /* skip the upper triangle */
      if (i >= len1 - half) {
        size_t offset = i - (len1 - half);
        size_t c3;

        char2p = string2 + offset;
        p = row + offset;
        c3 = *(p++) + (char1 != *(char2p++));
        x = *p;
        x++;
        D = x;
        if (x > c3)
          x = c3;
        *(p++) = x;
      }
      else {
        p = row + 1;
        char2p = string2;
        D = x = i;
      }
      /* skip the lower triangle */
      if (i <= half + 1)
        end = row + len2 + i - half - 2;
      /* main */
      while (p <= end) {
        size_t c3 = --D + (char1 != *(char2p++));
        x++;
        if (x > c3)
          x = c3;
        D = *p;
        D++;
        if (x > D)
          x = D;
        *(p++) = x;
      }
      /* lower triangle sentinel */
      if (i <= half) {
        size_t c3 = --D + (char1 != *char2p);
        x++;
        if (x > c3)
          x = c3;
        *p = x;
      }
    }
  }

  i = *end;
  //free(row);
  return i;
}

float levenshtein_distance(struct binding* this  __attribute__((unused)), 
			   wchar_t **seg1, wchar_t **seg2) {
  size_t len1;
  size_t len2;
  size_t d;

  len1 = seg_len(seg1);
  len2 = seg_len(seg2);
  
  d = lev_edit_distance(len1, *seg1, len2, *seg2);
  
  return (float) d / (len1 > len2 ? (float)len1 : (float)len2);
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
  p->p_dist->b_sign = "D:levenshtein";
  p->p_dist->run = levenshtein_distance;
  return 0;
}
