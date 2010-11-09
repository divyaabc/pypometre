#include "matrix.h"

#include <string.h>
#include <stdlib.h>
#include <png.h>

#define BUF_SIZE 16
static float one_buf[BUF_SIZE] = 
  {1.0f, 1.0f, 1.0f, 1.0f,1.0f, 1.0f, 1.0f, 1.0f,
   1.0f, 1.0f, 1.0f, 1.0f,1.0f, 1.0f, 1.0f, 1.0f}; 

struct matrix* matrix_init(size_t nr, size_t nc) {
  struct matrix *m;
  size_t i, n;
  m = (struct matrix*) malloc(sizeof(struct matrix));
  m->m_size = nr > nc ? nr : nc;
  m->m_rows = nr;
  m->m_cols = nc;
  m->m_data = (float**)malloc(m->m_size*sizeof(float*));
  n = (((m->m_size*m->m_size)/BUF_SIZE)+1) * BUF_SIZE;
  m->m_storage = (float*)malloc(n *sizeof(float*));
  
  for (i = 0; i < m->m_size; ++i) {
    m->m_data[i] = m->m_storage+i*m->m_size;
  }

  return m;
}

void matrix_fill(struct matrix* m, float v) {
  size_t i;
  for (i = 0; i < m->m_size*m->m_size; ++i) {
    m->m_storage[i] = v;
  }
}

#include <wchar.h>
void matrix_fill_one(struct matrix* m) {
  if (sizeof(float) == sizeof(wchar_t)) {
    static float one = 1.0f;
    wmemset((wchar_t*)m->m_storage, *((wchar_t*) &one), m->m_size*m->m_size);
  } else {
    size_t i, n = (m->m_size*m->m_size)/BUF_SIZE;
    for (i = 0; i <= n; ++i) { 
      memcpy(m->m_storage+i*BUF_SIZE, one_buf, BUF_SIZE*sizeof(float));
    }
  }
}

void matrix_copy(struct matrix *dst, struct matrix *src) {
  dst->m_rows = src->m_rows;
  dst->m_cols = src->m_cols;
  dst->m_size = src->m_size;

  //memcpy(dst->m_data, src->m_data, dst->m_size*sizeof(float*));
  memcpy(dst->m_storage, src->m_storage, dst->m_size*dst->m_size*sizeof(float));
}


void do_matrix_delete(struct matrix* m) {
  free(m->m_data);
  free(m->m_storage);
  // free(m);
}


int matrix_to_png(struct matrix *m, const char * filename) {
  unsigned int n = m->m_size;
  png_structp png_ptr;
  png_infop info_ptr;
  png_bytep row_pointers[n];
  const int bpp = 1;
  png_byte vals[n*n*bpp];
  unsigned int i, j;


  for( i = 0; i < n; ++i) { 
    row_pointers[i] = &(vals[i*n*bpp]);
    //png_byte* ptr = &(row[x*4]);
    for( j = 0; j < n; ++j) {
      char v = 255 - (char)(m->m_data[i][j]*255);
      vals[(i*n+j)*bpp] = (png_byte)v;
    }
  }
    
  FILE *fp = fopen(filename, "wb");
  png_ptr = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
  info_ptr = png_create_info_struct(png_ptr);
  setjmp(png_jmpbuf(png_ptr));
  png_init_io(png_ptr, fp);
  setjmp(png_jmpbuf(png_ptr));
  png_set_IHDR(png_ptr, info_ptr, n, n,
	       8, PNG_COLOR_TYPE_GRAY, PNG_INTERLACE_NONE,
	       PNG_COMPRESSION_TYPE_BASE, PNG_FILTER_TYPE_BASE);
  png_write_info(png_ptr, info_ptr);
  setjmp(png_jmpbuf(png_ptr));
  png_write_image(png_ptr, row_pointers);
  setjmp(png_jmpbuf(png_ptr));
  png_write_end(png_ptr, NULL);
    
  png_destroy_write_struct(&png_ptr, &info_ptr);
  fclose(fp);
    
  return 1;

}
