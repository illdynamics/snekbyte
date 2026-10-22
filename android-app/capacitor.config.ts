import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.illdynamics.snekbyte',
  appName: 'SnekByte',
  webDir: 'www',
  bundledWebRuntime: false,
  android: {
    allowMixedContent: false,
    captureInput: true,
    webContentsDebuggingEnabled: false
  },
  server: {
    androidScheme: 'https'
  },
  plugins: {
    App: {
      // The game shows its own pause overlay; do not let the system
      // terminate the WebView back stack before JS handles the Back key.
      disableBackButtonHandler: false
    }
  }
};

export default config;
