package com.integration.java_producers.model;

public class CustomerPayload {
    private String rawData;

    public CustomerPayload(String rawData) {
        this.rawData = rawData;
    }

    public String getRawData() {
        return rawData;
    }
}
