package com.integration.java_producers.model;

public class InventoryPayload {
    private String rawData;

    public InventoryPayload(String rawData) {
        this.rawData = rawData;
    }

    public String getRawData() {
        return rawData;
    }
}
