//
//  0.c
//  211-723Smolskaya
//
//  Created by Виктория  Смольская  on 21.09.2021.
//

#include <stdio.h>

int main () {
    int a = 0;
    printf("Введите длину прямоугольника:");
    scanf("%d", &a);
    
    int b = 0;
    printf ("Введите ширину прямогольника:");
    scanf("%d", &b);
    int s = 0;
    s = a*b;
    printf ("Площадь прямоугольника = %d\n", s);
    return 0;
}
