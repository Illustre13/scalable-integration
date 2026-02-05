package com.integration.java_producers.service;

import com.integration.java_producers.client.InventoryClient;
import com.integration.java_producers.model.CanonicalEvent;
import com.integration.java_producers.model.InventoryPayload;
import com.integration.java_producers.publisher.EventPublisher;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;

@Service
public class InventoryProducerService {

    private final InventoryClient inventoryClient;
    private final EventPublisher publisher;

    public InventoryProducerService(InventoryClient inventoryClient, EventPublisher publisher) {
        this.inventoryClient = inventoryClient;
        this.publisher = publisher;
    }

    @Retryable(
        maxAttempts = 3,
        backoff = @Backoff(delay = 2000)
    )
    public void produceInventory() {
        String response = inventoryClient.fetchInventory();

        CanonicalEvent<InventoryPayload> event =
                new CanonicalEvent<>("INVENTORY", new InventoryPayload(response));

        publisher.publishInventoryEvent(event);
    }
}
