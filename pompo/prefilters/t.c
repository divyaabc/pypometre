#include <wchar.h>
#include <wctype.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "profile.h"
#include "file.h"

struct textinfo* t_prefilter(struct binding* self, struct file* f) {
  wchar_t* t = (wchar_t*) self->b_data;
  int off;
  wchar_t *src, *dst, *text;
  size_t len = 0;

  off  = wcslen(t);

  dst = text = (wchar_t*) malloc((off*f->f_orig.ti_len+1)*sizeof(wchar_t));
  src = f->f_orig.ti_text;

  while (*src) {
    if (iswalpha(*src) || *src == L'_') {
      wcscpy(dst, t);
      dst += off;
      len += off;
      for (++src; iswalnum(*src) || *src == L'_'; ++src);
    } else {
      *dst++ = *src++;   
      ++len;   
    }
  }
  *dst = L'\0';
  
  return textinfo_make(self->b_sign, text, len);
}

void module_loader(void) {
}

void module_unbinder(struct profile* p) {
  if (p->p_prefilt == NULL) return;
  free(p->p_prefilt->b_data);
  free(p->p_prefilt->b_sign);
  free(p->p_prefilt);
  p->p_prefilt = NULL;
}

int module_binder(const char* args, struct profile* p) {
  wchar_t* t;
  int n = 2;
  
  if (p->p_prefilt != NULL) {
    fprintf(stderr, "unable to bind module: Prefiltering module already bound\n");
    return -1;
  }

  p->p_prefilt = (struct binding*) malloc(sizeof(struct binding));;
  
  if (args != NULL) {
    n = strlen(args) + 1;
    t = malloc(n * sizeof(wchar_t));
    mbstowcs(t, args, strlen(args) + 1);
  } else {
    t = (void*) wcsdup(L"t");    
  }

  p->p_prefilt->b_sign = (char*) malloc((2+n)*sizeof(char));
  sprintf(p->p_prefilt->b_sign, "T:%ls", t);
  p->p_prefilt->b_data = (void*) t;
  p->p_prefilt->run = t_prefilter;

  return 0;
}
