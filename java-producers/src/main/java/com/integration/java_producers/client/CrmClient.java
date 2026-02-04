package com.integration.java_producers.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class CrmClient {

    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${producer.crm.base-url}")
    private String baseUrl;

    public String fetchCustomers() {
        return restTemplate.getForObject(
                baseUrl + "/customers",
                String.class
        );
    }
}
