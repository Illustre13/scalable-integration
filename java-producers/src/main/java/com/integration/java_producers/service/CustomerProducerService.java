package com.integration.java_producers.service;

import com.integration.java_producers.client.CrmClient;
import com.integration.java_producers.model.CanonicalEvent;
import com.integration.java_producers.model.CustomerPayload;
import com.integration.java_producers.publisher.EventPublisher;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;

@Service
public class CustomerProducerService {

    private final CrmClient crmClient;
    private final EventPublisher publisher;

    public CustomerProducerService(CrmClient crmClient, EventPublisher publisher) {
        this.crmClient = crmClient;
        this.publisher = publisher;
    }

    @Retryable(
        maxAttempts = 3,
        backoff = @Backoff(delay = 2000)
    )
    public void produceCustomers() {
        String response = crmClient.fetchCustomers();

        CanonicalEvent<CustomerPayload> event =
                new CanonicalEvent<>("CRM", new CustomerPayload(response));

        publisher.publishCustomerEvent(event);
    }
}
