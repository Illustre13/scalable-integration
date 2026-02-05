package com.integration.java_producers.model;

import java.time.Instant;

public class CanonicalEvent<T> {

    private String source;
    private Instant timestamp;
    private T payload;

    public CanonicalEvent(String source, T payload) {
        this.source = source;
        this.payload = payload;
        this.timestamp = Instant.now();
    }

    public String getSource() {
        return source;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public T getPayload() {
        return payload;
    }
}
