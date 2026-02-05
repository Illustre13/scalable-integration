package com.integration.java_producers.model;

import java.io.Serializable;

public class CustomerPayload implements Serializable {
    private static final long serialVersionUID = 1L;

    private String rawData;

    public CustomerPayload(String rawData) {
        this.rawData = rawData;
    }

    public String getRawData() {
        return rawData;
    }
}
