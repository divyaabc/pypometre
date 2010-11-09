#include "module.h"
#include "pompo.h"
#include <dlfcn.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

extern int verbosity;

static struct module *modules = NULL;

typedef void (*modloader_t)(void);

struct module* module_load(const char* filename) {
  struct module* mod;
  modloader_t loader;

  LOG(1) printf("loading module: %s ...", filename);

  mod = (struct module*) malloc(sizeof(struct module));
  LOG(1) fflush(stdout);
  if ((mod->handle = dlopen(filename, RTLD_NOW|RTLD_LOCAL)) == NULL) {
    fprintf(stderr, "%s\n", dlerror());
    LOG(1) puts("failed.");
    free(mod);
    return NULL;
  }

  if ((loader = (modloader_t) dlsym(mod->handle, "module_loader")) == NULL) {
    fprintf(stderr, "invalid module %s\n", filename);
    LOG(1) printf("failed ");
    dlclose(mod->handle);
    free(mod);
    return NULL;
  }

  if ((mod->bind = (modbinder_t) dlsym(mod->handle, "module_binder")) == NULL) {
    fprintf(stderr, "invalid module %s\n", filename);
    LOG(1) printf("failed ");
    dlclose(mod->handle);
    free(mod);
    return NULL;
  }

 if ((mod->unbind = (modunbinder_t) dlsym(mod->handle, "module_unbinder")) == NULL) {
    fprintf(stderr, "invalid module %s\n", filename);
    LOG(1) printf("failed ");
    dlclose(mod->handle);
    free(mod);
    return NULL;
  }

  /* silently ignore error if no unloader is present */
  mod->unload = (modunloader_t) dlsym(mod->handle, "module_unloader");

  loader();

  LOG(1) puts("done.");

  mod->next = modules;
  mod->filename = strdup(filename);
  mod->bindings = NULL;
  modules = mod;

  return mod;
}

int module_bind(struct module* m, const char* args, struct profile* prof) {
  struct mod_binding* b;
  b = (struct mod_binding*) malloc(sizeof(struct mod_binding));
  b->next = m->bindings;
  b->profile = prof;
  m->bindings = b;
  return m->bind(args, prof);
}

void module_unbind(struct module* m, struct profile* prof) {
  struct mod_binding *b, *prev = NULL;
  b = m->bindings;
  while (b != NULL) {
    if (b->profile == prof) {
      m->unbind(prof);
      if (prev != NULL) {
	prev->next = b->next;
      } else {
	m->bindings = b->next;
      }
      free(b);
      break;
    }
    prev = b;
    b = b->next;
  }
}

void module_unbind_all(struct module* m) {
  struct mod_binding* b;
  b = m->bindings;
  while (b != NULL) {
    struct mod_binding* tmp = b;
    m->unbind(b->profile);
    b = b->next;
    free(tmp);
  }
}

void module_unload_all() {
  struct module* mod;
  mod = modules;
  //puts("unloading all modules:");
  while (mod != NULL) {
    struct module* tmp = mod;
    LOG(1) printf("unloading %s ...", mod->filename);
    fflush(stdout);
    
    module_unbind_all(mod);

    if (mod->unload != NULL) {
      mod->unload();
    }

    dlclose(mod->handle);
    mod = mod->next;
    free(tmp->filename);
    free(tmp);
    LOG(1) printf(" done.\n");
  }
  modules = NULL;
}
