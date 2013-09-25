#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#define xmalloc malloc
#define xcalloc calloc
#define member_size(type, member) sizeof(((type *)0)->member)

typedef struct STRList {
  int64_t size;
  int8_t  **array;
} STRList;


STRList *allocSTRList(int64_t size) {
  STRList *list;
  list = xmalloc(sizeof(STRList));
  list->size  = size;
  list->array = xcalloc(size, member_size(STRList, array));
  return list;
}

STRList *printSTRList(STRList *list) {
  printf("[");
  for (int64_t i=0; i < list->size; i++) {
    printf("\"%s\",", list->array[0]);
  }
  printf("]\n");

  return list;
}

STRList *mainargs(int argc, char *argv[]) {
  STRList *list = allocSTRList(argc);
  list->array = argv;
  //for (int i=0; i<argc; i++){
  //  list->array[i] = argv[i];
  //}

  return list;
}

int main(int argc, char *argv[]) {
  STRList *list = mainargs(argc, argv);
  printSTRList(list);
  return 0;
}
