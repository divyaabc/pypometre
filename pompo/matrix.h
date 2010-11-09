#ifndef MATRIX_H
#define MATRIX_H

#include <stdlib.h>

struct matrix {
  float **m_data;
  float *m_storage;
  size_t m_rows;
  size_t m_cols;
  size_t m_size;
};

struct matrix* matrix_init(size_t nr, size_t nc);
struct matrix* matrix_init_val(size_t nr, size_t nc, float v);
void matrix_fill(struct matrix* m, float v);
void matrix_fill_one(struct matrix* m);
void matrix_copy(struct matrix *dst, struct matrix *src);
void do_matrix_delete(struct matrix* m);

#define matrix_delete(m) {do_matrix_delete(m); free(m);}

int matrix_to_png(struct matrix *m, const char * filename);

#endif //MATRIX_H
