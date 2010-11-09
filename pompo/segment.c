#include "segment.h"

size_t seg_len(wchar_t** seg) {
  return *(seg+1) - *seg;
}
