#include "file.h"
#include "profile.h"

#include <stdlib.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>

struct seginfo* nl_segmenter(struct binding* this, struct file* f, struct textinfo* ti) {
  wchar_t **segs, **s;
  wchar_t *cur;
  size_t n = 0;
  long group_size = 0;
  long groupby = *((long*)this->b_data);

  if (f == NULL || ti->ti_text == NULL) {
    return NULL;
  }

  if ((segs = (wchar_t**) malloc(ti->ti_len * sizeof(wchar_t*))) == NULL) {
    return NULL;
  }
  s = segs;
  *s++ = cur = ti->ti_text;
  while (*cur != L'\0') {
    if (*cur == L'\n' && ++group_size == groupby) {
      *s++ = cur+1; /* +1 : newline is part of segment */
      ++n;
      group_size = 0;
    }
    ++cur;
  }
  if (group_size) { /* incomplete last group */
    *s++ = cur+1;
    ++n;
  }
  *s = NULL;

  return seginfo_make(this->b_sign, ti, segs, n);
}

void module_loader(void) {
}

void module_unbinder(struct profile* p) {
  if (p->p_seg == NULL) {
    return;
  }

  free(p->p_seg->b_sign);
  free(p->p_seg->b_data);
  free(p->p_seg);
  p->p_seg = NULL;
}

int module_binder(const char* args, struct profile* p) {
  long *groupby;
  groupby = (long*) malloc(sizeof(long));

  if (p->p_seg != NULL) {
    fprintf(stderr, "unable to bind module: Segmenter module already bound\n");
    return -1;
  }

  p->p_seg = (struct binding*) malloc(sizeof(struct binding));

  if (args != NULL) {
    char *end;
    long group;
    errno = 0;
    group = strtol(args, &end, 10);
    if ((errno == ERANGE && (group == LONG_MAX || group == LONG_MIN))
            || (errno != 0 && group == 0)) {
      fprintf(stderr, "newline: parameter '%s' out of range\n", args);
    } else if (end == args) {
      fprintf(stderr, "newline: parameter '%s' is not an integer\n", args);
    } else {
      if (group < 1) {
	fprintf(stderr, "newline: parameter '%s' must be strictly positive\n", args);
      } else {
	*groupby = group;
      }
    }
  }
  p->p_seg->run = nl_segmenter;
  p->p_seg->b_data = (void**) groupby;
  p->p_seg->b_sign = (char*) malloc(64*sizeof(char)); //FIXME: add to bind data to avoid a leak !!
  snprintf(p->p_seg->b_sign, 63, "NL:%ld", *groupby);
  return 0;
}
