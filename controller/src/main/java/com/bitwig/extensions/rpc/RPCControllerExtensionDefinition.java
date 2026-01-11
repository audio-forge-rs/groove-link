package com.bitwig.extensions.rpc;

import java.util.UUID;

import com.bitwig.extension.api.PlatformType;
import com.bitwig.extension.controller.AutoDetectionMidiPortNamesList;
import com.bitwig.extension.controller.ControllerExtensionDefinition;
import com.bitwig.extension.controller.api.ControllerHost;

public class RPCControllerExtensionDefinition extends ControllerExtensionDefinition {

    private static final UUID DRIVER_ID = UUID.fromString("a1b2c3d4-e5f6-7890-abcd-ef1234567890");

    public RPCControllerExtensionDefinition() {
    }

    @Override
    public String getName() {
        return "JSON-RPC/OSC";
    }

    @Override
    public String getAuthor() {
        return "Claude Opus 4.5";
    }

    @Override
    public String getVersion() {
        return RPCControllerExtension.VERSION;
    }

    @Override
    public UUID getId() {
        return DRIVER_ID;
    }

    @Override
    public String getHardwareVendor() {
        return "Audio Forge RS";
    }

    @Override
    public String getHardwareModel() {
        return "JSON-RPC/OSC";
    }

    @Override
    public int getRequiredAPIVersion() {
        return 19;
    }

    @Override
    public int getNumMidiInPorts() {
        return 0;
    }

    @Override
    public int getNumMidiOutPorts() {
        return 0;
    }

    @Override
    public void listAutoDetectionMidiPortNames(
            AutoDetectionMidiPortNamesList list, PlatformType platformType) {
        // No MIDI ports - this is a network controller
    }

    @Override
    public RPCControllerExtension createInstance(ControllerHost host) {
        return new RPCControllerExtension(this, host);
    }
}
