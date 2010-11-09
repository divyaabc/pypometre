#include "file.h"

#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include "pompo.h"

extern int verbosity;

struct file* file_load(const char* filename) {
  struct file* f;
  struct stat st;
  char* buf, *ptr;
  int fd;
  size_t n, len;
  mbstate_t state;
  size_t nbytes;
  wchar_t* txt;

  if (filename == NULL) {
    return NULL;
  }

  if ((f = (struct file*) malloc(sizeof(struct file))) == NULL) {
    return NULL;
  }

  if (stat(filename, &st) < 0) {
    free(f);
    perror(filename);
    return NULL;
  }

  n = st.st_size + 1;
  if ((buf = (char*) malloc(n * (sizeof(char)))) == NULL) {
    free(f);
    return NULL;
  }
  
  if ((fd = open(filename, O_RDONLY)) < 0) {
    perror("open");
    free(f);
    free(buf);
    return NULL;
  }

  if (read(fd, buf, n - 1) < 0) {
    perror("read");
    free(f);
    free(buf);
    close(fd);
    return NULL;
  }

  close(fd);

  if ((f->f_orig.ti_text = (wchar_t*) malloc(n * sizeof(wchar_t))) == NULL) {
    free(f);
    free(buf);
    return NULL;
  }

  buf[n-1] = '\0'; /* mbsrtowcs requires NUL-terminated strings */  
  memset(&state, '\0', sizeof (state));
  len = n;
  txt = f->f_orig.ti_text;
  ptr = buf;
  f->f_orig.ti_len = 0;
  while ((nbytes = mbrtowc(txt, ptr, len, &state)) > 0) {
    if (nbytes >= (size_t) -2) {
      memset(&state, '\0', sizeof (state));
      ++ptr;
      --len;
      LOG(1) printf("skipping unreadable character in %s\n", filename);
      continue;
    }
    len -= nbytes;
    ptr += nbytes;
    ++f->f_orig.ti_len;
    ++txt;
  }
  
  /* if ((f->f_orig.ti_len = mbstowcs(f->f_orig.ti_text, buf, n)) == (size_t) -1) { */
  /*   fprintf(stderr, "error while reading %s\n", filename); */
  /*   perror("mbsrtowcs"); */
  /*   free(f->f_orig.ti_text); */
  /*   free(f); */
  /*   free(buf); */
  /*   return NULL; */
  /* } */
  
  free(buf);

  f->f_name = strdup(filename);
  f->f_segs = NULL;
  f->f_texts = NULL;
  return f;
}

void file_unload(struct file* f) {
  if (f == NULL) {
    return;
  }
  if (f->f_name != NULL) {
    free(f->f_name);
  }
  if (f->f_orig.ti_text != NULL) {
    free(f->f_orig.ti_text);
  }


  struct textinfo *tt,*t = f->f_texts;
  while(t != NULL) {    
    tt = t->next;
    free(t->ti_text);
    free(t);
    t = tt;
  }

  struct seginfo *ss,*s = f->f_segs;
  while(s != NULL) {    
    ss = s->next;
    free(s->si_segs);
    free(s);
    s = ss;
  }

  free(f);
}

struct textinfo* file_find_text(struct file* f, const char* sign) {
  struct textinfo* ti;
  ti = f->f_texts;
  while (ti != NULL) {
    if (!strcmp(sign, ti->ti_sign)) {
      return ti;
    }
    ti = ti->next;
  }
  return NULL;
}

void file_add_text(struct file* f, struct textinfo* ti) {
  textinfo_insert(&f->f_texts, ti);
}

struct textinfo* textinfo_make(char* sign, wchar_t* text, size_t len) {
  struct textinfo* ti;
  ti = (struct textinfo*) malloc(sizeof(struct textinfo));
  ti->ti_sign = sign;
  ti->ti_text = text;
  ti->ti_len  = len;
  return ti;
}

void textinfo_insert(struct textinfo** list, struct textinfo* ti) {
  ti->next = *list;
  *list = ti;
}

void file_add_seg(struct file* f, struct seginfo* si) {
  seginfo_insert(&f->f_segs, si);
}

struct seginfo* file_find_seg(struct file* f, const char* sign, struct textinfo* ti) {
  struct seginfo* si;
  si = f->f_segs;
  while (si != NULL) {
    if (!strcmp(sign, si->si_sign) && si->si_text == ti) {
      return si;
    }
    si = si->next;
  }
  return NULL;
}

struct seginfo* seginfo_make(char* sign, struct textinfo* text, wchar_t** segs, size_t size) {
  struct seginfo* si;
  si = (struct seginfo*) malloc(sizeof(struct seginfo));
  si->si_sign = sign;
  si->si_text = text;
  si->si_segs = segs;
  si->si_size = size;
  return si;
}
void seginfo_insert(struct seginfo** list, struct seginfo* si) {
  si->next = *list;
  *list = si;
}
