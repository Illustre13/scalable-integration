package com.integration.java_producers.publisher;

import com.integration.java_producers.config.RabbitMQConfig;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.GetMapping;

@Component
public class EventPublisher {

    private final RabbitTemplate rabbitTemplate;

    public EventPublisher(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public void publishCustomerEvent(Object event) {
        rabbitTemplate.convertAndSend(
                RabbitMQConfig.CUSTOMER_QUEUE, // using the constant for the customer queue
                event
        );
    }

    public void publishInventoryEvent(Object event) {
        rabbitTemplate.convertAndSend(RabbitMQConfig.INVENTORY_QUEUE, event); 
        //still passing the string here ...................
        // both ways stillll works ....
    }

    // @GetMapping("/send-test")
    // public String sendTest() {
    //     rabbitTemplate.convertAndSend("New Queue Event", "Hello RabbitMQ!");
    //     return "Message sent!";
    // }
}
