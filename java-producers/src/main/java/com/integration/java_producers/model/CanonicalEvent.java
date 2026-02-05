package com.integration.java_producers.model;

import java.time.Instant;
import java.io.Serializable;
public class CanonicalEvent<T> implements Serializable {
    private static final long serialVersionUID = 1L;

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
