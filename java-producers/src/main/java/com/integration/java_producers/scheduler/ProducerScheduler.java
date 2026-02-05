package com.integration.java_producers.scheduler;

import com.integration.java_producers.service.CustomerProducerService;
import com.integration.java_producers.service.InventoryProducerService;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
@EnableScheduling
public class ProducerScheduler {

    private final CustomerProducerService customerProducer;
    private final InventoryProducerService inventoryProducer;

    public ProducerScheduler(CustomerProducerService customerProducer,
                             InventoryProducerService inventoryProducer) {
        this.customerProducer = customerProducer;
        this.inventoryProducer = inventoryProducer;
    }

    @Scheduled(fixedRate = 60000)
    public void runProducers() {
        customerProducer.produceCustomers();
        inventoryProducer.produceInventory();
    }
}
