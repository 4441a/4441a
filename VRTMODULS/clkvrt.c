#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"
#include "hardware/timer.h"

#define CLOCK_IN_PIN 2
#define RESET_IN_PIN 19
#define NUM_MULTIPLIERS 7
#define NUM_LOGIC_OUTPUTS 9

const uint clock_multipliers[NUM_MULTIPLIERS] = {4, 3, 2, 1, 0.75, 0.5, 0.25};
const uint multiplier_outputs[NUM_MULTIPLIERS] = {3, 4, 5, 6, 7, 8, 9};
const uint logic_outputs[NUM_LOGIC_OUTPUTS] = {10, 11, 12, 13, 14, 15, 16, 17, 18};
const uint adc_channels[3] = {26, 27, 28};

volatile uint64_t last_clock_time = 0;
volatile uint64_t period = 500000;
volatile uint counter = 0;
volatile uint P, Q, R;

void clock_interrupt(uint gpio, uint32_t events) {
    uint64_t current_time = time_us_64();
    period = current_time - last_clock_time;
    last_clock_time = current_time;
    counter = 0;  // Reset counter on clock input
}

void reset_interrupt(uint gpio, uint32_t events) {
    counter = 0;
}

void update_gpio_states() {
    bool p_and_q = P & Q;
    bool p_or_q = P | Q;
    bool p_or_q_or_r = P | Q | R;
    bool not_p_and_q = !(P & Q);
    bool p_and_q_or_r = P & (Q | R);
    bool p_or_q_and_r_and_q = (P | Q) & (R & Q);
    bool p_and_q_alt = P & Q;
    bool p_or_q_and_not_q_and_p = (P | Q) & !(Q & P);
    bool p_or_q_and_not_p_and_q = (P | Q) & !(P & Q);

    bool logic_values[NUM_LOGIC_OUTPUTS] = {
        p_and_q, p_or_q, p_or_q_or_r, not_p_and_q,
        p_and_q_or_r, p_or_q_and_r_and_q, p_and_q_alt,
        p_or_q_and_not_q_and_p, p_or_q_and_not_p_and_q
    };

    for (int i = 0; i < NUM_LOGIC_OUTPUTS; i++) {
        gpio_put(logic_outputs[i], logic_values[i]);
    }
}

void generate_gates() {
    uint64_t half_period;
    for (int i = 0; i < NUM_MULTIPLIERS; i++) {
        half_period = (uint64_t)(period / (2 * clock_multipliers[i]));
        gpio_put(multiplier_outputs[i], 1);
        sleep_us(half_period);
        gpio_put(multiplier_outputs[i], 0);
        sleep_us(half_period);
    }
}

void read_sliders() {
    adc_select_input(0);
    uint p_index = adc_read() / 512;
    adc_select_input(1);
    uint q_index = adc_read() / 512;
    adc_select_input(2);
    uint r_index = adc_read() / 512;
    
    P = clock_multipliers[p_index];
    Q = clock_multipliers[q_index];
    R = clock_multipliers[r_index];
}

int main() {
    stdio_init_all();
    gpio_set_irq_enabled_with_callback(CLOCK_IN_PIN, GPIO_IRQ_EDGE_RISE, true, &clock_interrupt);
    gpio_set_irq_enabled_with_callback(RESET_IN_PIN, GPIO_IRQ_EDGE_RISE, true, &reset_interrupt);
    
    gpio_init(RESET_IN_PIN);
    gpio_set_dir(RESET_IN_PIN, GPIO_IN);
    gpio_pull_down(RESET_IN_PIN);
    
    for (int i = 0; i < NUM_MULTIPLIERS; i++) {
        gpio_init(multiplier_outputs[i]);
        gpio_set_dir(multiplier_outputs[i], GPIO_OUT);
    }
    
    for (int i = 0; i < NUM_LOGIC_OUTPUTS; i++) {
        gpio_init(logic_outputs[i]);
        gpio_set_dir(logic_outputs[i], GPIO_OUT);
    }

    adc_init();
    for (int i = 0; i < 3; i++) {
        adc_gpio_init(adc_channels[i]);
    }

    while (1) {
        read_sliders();
        update_gpio_states();
        generate_gates();
        sleep_ms(10);
    }
}
