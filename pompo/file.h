#ifndef FILE_H
#define FILE_H
#include <wchar.h>

struct textinfo {
  char*    ti_sign;
  wchar_t* ti_text;
  size_t   ti_len;
  struct textinfo* next;
};

struct textinfo* textinfo_make(char* sign, wchar_t* text, size_t len);
void textinfo_insert(struct textinfo** list, struct textinfo* ti);

struct seginfo {
  char*            si_sign;
  struct textinfo* si_text;
  wchar_t**        si_segs;
  size_t           si_size;
  struct seginfo* next;
};

struct seginfo* seginfo_make(char* sign, struct textinfo* text, wchar_t** segs, size_t size);
void seginfo_insert(struct seginfo** list, struct seginfo* ti);

struct file {
  char* f_name;
  struct textinfo  f_orig;
  struct textinfo* f_texts;
  struct seginfo*  f_segs;
};

struct file* file_load(const char* filename);
void file_unload(struct file* f);



struct textinfo* file_find_text(struct file* f, const char* sign);
void file_add_text(struct file* f, struct textinfo* ti);
struct seginfo* file_find_seg(struct file* f, const char* sign, struct textinfo* ti);
void file_add_seg(struct file* f, struct seginfo* si);
#endif
