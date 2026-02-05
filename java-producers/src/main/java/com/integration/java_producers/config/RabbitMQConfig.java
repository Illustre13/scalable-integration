package com.integration.java_producers.config;

// import java.util.Queue; -- using the correct AMQP lib for RabbitMQ integration
import org.springframework.amqp.core.Queue;


import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {

    public static final String CUSTOMER_QUEUE = "customer_data";
    // public static final String INVENTORY_QUEUE = "inventory_data";

    @Bean
    public Queue customerQueue() {
        return new Queue(CUSTOMER_QUEUE, true);
    }

    @Bean
    public Queue inventoryQueue() {
        return new Queue("inventory_data", true);
    }
}
