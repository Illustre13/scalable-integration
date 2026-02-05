package com.integration.java_producers.config;

// import java.util.Queue; -- using the correct AMQP lib for RabbitMQ integration
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

@Configuration
public class RabbitMQConfig {

    public static final String CUSTOMER_QUEUE = "customer_data";
    public static final String INVENTORY_QUEUE = "inventory_data";

    @Bean
    public Queue customerQueue() {
        return new Queue(CUSTOMER_QUEUE, true);
    }

    @Bean
    public Queue inventoryQueue() {
        // return new Queue("inventory_data", true);
        return new Queue(INVENTORY_QUEUE, true);
    }

    /**
     * Configure JSON message converter for RabbitMQ.
     * This ensures messages are serialized as JSON instead of Java binary format,
     * making them compatible with Python consumers.
     * Includes JavaTimeModule to support Java 8 date/time types (Instant, LocalDateTime, etc.)
     */
    @Bean
    public MessageConverter jsonMessageConverter() {
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.registerModule(new JavaTimeModule());
        return new Jackson2JsonMessageConverter(objectMapper);
    }

    /**
     * Configure RabbitTemplate to use JSON converter.
     */
    @Bean
    public RabbitTemplate rabbitTemplate(ConnectionFactory connectionFactory) {
        RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory);
        rabbitTemplate.setMessageConverter(jsonMessageConverter());
        return rabbitTemplate;
    }
}
