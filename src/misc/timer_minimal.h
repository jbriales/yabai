#ifndef TIMER_MINIMAL_H
#define TIMER_MINIMAL_H

#include <stdint.h>
#include <stdio.h>
#include <time.h>

static inline uint64_t read_cpu_timer(void)
{
#ifdef __x86_64__
    return __rdtsc();
#elif __arm64__
    uint64_t value;
    __asm__ __volatile__ ("mrs %0, cntvct_el0" : "=r" (value));
    return value;
#endif
}

static inline uint64_t read_cpu_freq(void)
{
#ifdef __x86_64__
    static uint64_t cpu_freq;
    if (cpu_freq == 0) {
        uint64_t ms_to_wait   = 100;
        uint64_t os_freq      = read_os_freq();
        uint64_t cpu_start    = read_cpu_timer();
        uint64_t os_start     = read_os_timer();
        uint64_t os_end       = 0;
        uint64_t os_elapsed   = 0;
        uint64_t os_wait_time = os_freq * ms_to_wait / 1000;

        while (os_elapsed < os_wait_time) {
            os_end     = read_os_timer();
            os_elapsed = os_end - os_start;
        }

        uint64_t cpu_end     = read_cpu_timer();
        uint64_t cpu_elapsed = cpu_end - cpu_start;

        cpu_freq = os_freq * cpu_elapsed / os_elapsed;
    }
    return cpu_freq;
#elif __arm64__
    uint64_t value;
    __asm__ __volatile__ ("mrs %0, cntfrq_el0" : "=r" (value));
    return value;
#endif
}

struct simple_profile
{
    char const *label;
    uint64_t start_timestamp;
    uint64_t final_timestamp;
};

time_t get_unix_timestamp() {
    return time(NULL);  // Get the current Unix timestamp
    // NOTE: -1 if failed to get the time
}

static void begin_simple_profile(struct simple_profile *profile, char const *label)
{
    profile->label = label;
    profile->start_timestamp = read_cpu_timer();
}

static void end_simple_profile_and_print(struct simple_profile *profile, char const *function_name)
{
    profile->final_timestamp = read_cpu_timer();
    uint64_t timer_freq = read_cpu_freq();
    printf("PROFILE | %ld | %0.4fms | %s |  %s \n", get_unix_timestamp(), 1000.0 * (double)(profile->final_timestamp - profile->start_timestamp) / (double)timer_freq, function_name, profile->label);
}

#endif
