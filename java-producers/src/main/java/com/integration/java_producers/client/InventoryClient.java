package com.integration.java_producers.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class InventoryClient {

    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${producer.inventory.base-url}")
    private String baseUrl;

    public String fetchInventory() {
        return restTemplate.getForObject(
                baseUrl + "/products",
                String.class
        );
    }
}
