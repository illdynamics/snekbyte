package com.illdynamics.snekbyte;

import android.graphics.Color;
import android.os.Bundle;
import android.view.Window;

import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsControllerCompat;

import com.getcapacitor.BridgeActivity;

/**
 * SnekByte entry activity.
 *
 * Keeps the default Capacitor secure WebViewAssetLoader behaviour and only adds
 * SnekByte visual polish:
 *   - edge-to-edge drawing so the dark game background reaches the system bars,
 *   - light system-bar icons (dark game background),
 *   - transparent status/navigation bars.
 *
 * The bundled PWA uses viewport-fit=cover + env(safe-area-inset-*) so the
 * D-pad, Poop-o-meter and settings sheet never slide under system controls.
 */
public class MainActivity extends BridgeActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        configureSystemBars();
    }

    private void configureSystemBars() {
        Window window = getWindow();
        WindowCompat.setDecorFitsSystemWindows(window, false);

        WindowInsetsControllerCompat controller =
                WindowCompat.getInsetsController(window, window.getDecorView());
        if (controller != null) {
            controller.setAppearanceLightStatusBars(false);
            controller.setAppearanceLightNavigationBars(false);
        }

        window.setStatusBarColor(Color.TRANSPARENT);
        window.setNavigationBarColor(Color.TRANSPARENT);
    }
}
