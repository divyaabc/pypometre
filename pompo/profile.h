#ifndef PROFILE_H
#define PROFILE_H

#include "file.h"
#include "matrix.h"

#define ERR_PREFILTER -1
#define ERR_SEGEMENTER -2
#define ERR_DISTANCE -3

#define ERR_INVALID_PROFILE -255

struct binding {
  char* b_sign;
  void* b_data;
  void* run;
};

struct profile;

struct textinfo* profile_run_prefilt(struct profile* p, struct file* f);
struct seginfo*  profile_run_seg(struct profile* p, struct file* f, struct textinfo* ti);

typedef struct textinfo* (*prefilt_t)(struct binding*, struct file*);
typedef struct seginfo* (*seg_t)(struct binding*, struct file*, struct textinfo*);
typedef float (*dist_t)(struct binding*, wchar_t**, wchar_t**);
typedef float (*docdist_t)(struct binding*, struct matrix*);

struct profile {
  struct binding* p_prefilt;
  struct binding* p_seg;
  struct binding* p_dist;
  struct binding* p_docdist;
};

void profile_init(struct profile* p);
int profile_check(struct profile* p);
struct matrix* profile_run(struct profile* p, struct file** files, int nf, int* pairs, int np);

#endif //PROFILE_H

