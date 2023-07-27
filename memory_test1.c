#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <time.h>

#define command_size 7 // размер ячейки команд для тестирования
#define addr_size 4 // размер адреса (int 4 байта)
#define lfsr_size 20 // количество бит для генерации адреса

// функция РСЛОС Фибоначчи
int LFSR_Fibonacci() {
    static unsigned long S = 0x00000001;
    S = ((((S >> 31) ^ (S >> 30) ^ (S >> 29) ^ (S >> 27) ^ (S >> 25) ^ S) & 0x00000001) << 31) | (S >> 1);
    return S & 0x00000001;
}

// фнукция подготовки памяти для тестирования (псевдослучайные переходы)
void asm_test_prepare1(char* pointer, int length) {
    unsigned char barr[addr_size]; // буффер для временного хранения байтов адреса прыжка
    unsigned int addr_base = &pointer[0];
    unsigned int addr = 0, addr_new, addr_offset; // переменные адреса прыжка
    unsigned short int bit0;
    unsigned char byte0;

    // генерация псевдослучайных прыжков
    for (int i = 0; i < length - command_size; i += command_size) {
        pointer[addr] = 0xb8; // mov ассемблерная команда (первый байт)

        pointer[addr + command_size - 2] = 0xff; // jmp/call ассемблерная команда (первый байт)
        pointer[addr + command_size - 1] = 0xe0; // jmp по адресу из eax (второй байт)

        addr_new = length;
        while (addr_new >= length) { // генерация псевдослучайного адреса
            addr_new = 0;
            for (int j = 0; j < lfsr_size; j++) { // 20 для 1MB
                bit0 = LFSR_Fibonacci();
                addr_new = (addr_new << 1) | bit0;
            }
            addr_new *= command_size;

            byte0 = pointer[addr_new];
            if (byte0 == 0xb8) // проверка заполнения ячейки
                addr_new = length;
        }

        addr_offset = addr_base + addr_new; // получение адреса для прыжка
        memcpy(barr, &addr_offset, addr_size); // перевод адреса из int в набор байтов

        for (unsigned int j = 0; j < addr_size; j++) // добавление адреса в eax
            pointer[addr + 1 + j] = barr[j]; // байты расположены от младшего к старшему, как в машинных кодах

        addr = addr_new; // присвоение нового адреса для обращения к ячейке

        if (i == length - command_size * 2) // в последней ячейке выход из функции
            pointer[addr] = 0xc3; // ret ассемблерная команда
    }

    return;
}

// фнукция подготовки памяти для тестирования (последовательные переходы)
void asm_test_prepare2(char *pointer, int length) {
    unsigned char barr[addr_size]; // буффер для временного хранения байтов адреса прыжка
    unsigned int addr; // переменная адреса прыжка

    // генерация последовательных прыжков
    for (int i = 0; i < length - command_size; i += command_size) {
        pointer[i] = 0xb8; // mov ассемблерная команда (первый байт)

        addr = &pointer[i + command_size]; // получение адреса для прыжка
        memcpy(barr, &addr, addr_size); // перевод адреса из int в набор байтов

        for (unsigned int j = 0; j < addr_size; j++) // добавление адреса в eax
            pointer[i + 1 + j] = barr[j]; // байты расположены от младшего к старшему, как в машинных кодах

        pointer[i + command_size - 2] = 0xff; // jmp/call ассемблерная команда (первый байт)
        pointer[i + command_size - 1] = 0xe0; // jmp по адресу из eax (второй байт)
    }
    pointer[length - command_size] = 0xc3; // команда возврата

    /*
    unsigned short int bit0;
    unsigned int addr_arr[2];
    unsigned char byte0;

    // перемешивание ячеек
    for (int i = 0; i < length; i += command_size) {

        // генерация псевдослучайных адресов для 2 ячеек
        for (int k = 0; k < 2; k++) {
            addr = length;
            while (addr >= length) {
                addr = 0;
                for (int j = 0; j < 20; j++) { // 20 for 1MB
                    bit0 = LFSR_Fibonacci();
                    addr = (addr << 1) | bit0;
                    //while(addr >= mem_len) {
                    //    bit0 = LFSR_Fibonacci();
                    //    addr = (addr << 1) | bit0;
                    //    addr = addr & 0x00001FFF; // 007FFFFF for 5MB
                    //}
                }
                addr *= command_size;
            }
            addr_arr[k] = addr;
        }

        // обмен адресов ячеек
        for (int j = 1; j < addr_size + 1; j++) {
            byte0 = pointer[addr_arr[0] + j];
            pointer[addr_arr[0] + j] = pointer[addr_arr[1] + j];
            pointer[addr_arr[1] + j] = byte0;
        }
    }*/

    return;
}

// функция тестирования
double asm_test_start(unsigned int pointer_addr) {
    double time;

    clock_t start_clock = clock(); // начало отсчёта
    __asm { // ассемблерная вставка
        mov eax, pointer_addr   // записать адрес в eax
        call eax                // call по адресу из eax
        mov time, 1             // запись 1 в переменную
    }
    clock_t end_clock = clock(); // конец отсчёта

    time = (double)(end_clock - start_clock) / CLOCKS_PER_SEC;
    return time;
}

// функция проверки количества переходов
int asm_test_check(char* pointer) {
    int jump_num = 0, i = 0;
    unsigned int addr = 0, pointer_addr = &pointer[0];
    unsigned char barr[addr_size]; // буффер для временного хранения байтов адреса прыжка

    while (1) {
        unsigned char bmov = pointer[i];
        unsigned short int bjmp = 0; // копирование значения первого байта
        barr[0] = pointer[i + command_size - 1];
        barr[1] = pointer[i + command_size - 2];
        memcpy(&bjmp, barr, 2); // копирование значения последних двух байтов

        if (bmov == 0xc3) // команда ret
            return jump_num + 1;
        else {
            if (bmov == 0xb8) { // команда mov
                for (unsigned int j = 0; j < addr_size; j++) // считывание адреса
                    barr[j] = pointer[i + 1 + j]; // байты расположены от младшего к старшему, как в машинных кодах
                memcpy(&addr, barr, addr_size); // перевод адреса из набора байтов в int
                addr -= pointer_addr; // вычитание смещения из адреса
            }
            else
                return -1;

            if (bjmp == 0xffe0) { // команда jmp
                jump_num++;
                i = addr;
            }
            else
                return -1;
        }
    }
}

// главная функция
int main() {
    const int mem_len = 1024 * 1024 * command_size; // размер памяти в байтах
    char* mem_ptr = (char*)malloc(mem_len); // выделение памяти

    if (mem_ptr == NULL) // выделение памяти не удалось
        return -1;

    asm_test_prepare1(mem_ptr, mem_len); // подготовка выделенной памяти для тестирования

    int asm_res = asm_test_check(mem_ptr); // проверка количества переходов в тесте
    printf("maximum test jumps: %d\n", mem_len / command_size); // вывод количества возможных переходов
    printf("real test jumps: %d\n", asm_res); // вывод количества переходов

    DWORD dummy; // что-то для virt protect, не трогать
    VirtualProtect(mem_ptr, mem_len, PAGE_EXECUTE, &dummy); // разрешить исполнение команд в выделенной памяти
    int asm_ptr = &mem_ptr[0]; // получение адреса для первого байта выделеннрй памяти
    double asm_time = asm_test_start(asm_ptr); // вызов функции тестирования
    VirtualProtect(mem_ptr, mem_len, PAGE_READWRITE, &dummy); // вернуть изначальные разрешения для выделенной памяти

    printf("test time: %f sec\n", asm_time); // вывод времени тестирования

    free(mem_ptr); // освобождение выделенной памяти

    system("pause");
    return 0;
}
