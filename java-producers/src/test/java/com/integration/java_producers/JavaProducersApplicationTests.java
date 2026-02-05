package com.integration.java_producers;

import org.junit.jupiter.api.Test;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

import com.integration.java_producers.client.InventoryClient;

@SpringBootTest
class JavaProducersApplicationTests {

    @MockitoBean
    private InventoryClient inventoryClient;

    @MockitoBean
    private RabbitTemplate rabbitTemplate;

    @Test
    void contextLoads() {}
}

