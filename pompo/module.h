#ifndef MODULE_H
#define MODULE_H

#include "profile.h"

typedef int (*modbinder_t)(const char *args, struct profile*);
typedef void (*modunloader_t)(void);
typedef char* (*modunbinder_t)(struct profile*);

struct mod_binding {
  struct profile *profile;
  struct mod_binding* next;
};

struct module {
  void* handle;
  char* filename;
  modbinder_t bind;
  modunbinder_t unbind;
  modunloader_t unload;
  struct mod_binding *bindings;
  struct module* next;
};

struct module* module_load(const char* filename);
int module_bind(struct module* m, const char* args, struct profile* prof);
void module_unbind(struct module* m, struct profile* prof);
void module_unbind_all(struct module* m);
void module_unload_all();

#endif //MODULE_H
