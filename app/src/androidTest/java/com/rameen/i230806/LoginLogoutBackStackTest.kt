package com.rameen.i230806

import android.app.Activity
import androidx.test.core.app.ActivityScenario
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.Espresso.pressBackUnconditionally
import androidx.test.espresso.action.ViewActions.click
import androidx.test.espresso.action.ViewActions.scrollTo
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.isDisplayed
import androidx.test.espresso.matcher.ViewMatchers.withId
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.runner.lifecycle.ActivityLifecycleMonitorRegistry
import androidx.test.runner.lifecycle.Stage
import com.rameen.i230806.ui.auth.LoginActivity
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Test 2 (back stack): Login -> Home -> Menu -> Log out -> Login, then Back leaves the app.
 */
@RunWith(AndroidJUnit4::class)
class LoginLogoutBackStackTest {

    @Test
    fun logoutClearsBackStack() {
        // Step 1: start the app on the Login screen.
        ActivityScenario.launch(LoginActivity::class.java).use {

            // Step 2: tap "Log in" and check the Home feed is showing.
            onView(withId(R.id.btn_login)).perform(click())
            onView(withId(R.id.tv_wordmark)).check(matches(isDisplayed()))

            // Step 3: open the Menu tab, scroll to "Log out" and tap it.
            onView(withId(R.id.fl_tab_menu)).perform(click())
            onView(withId(R.id.ll_logout)).perform(scrollTo(), click())

            // Step 4: the Login screen is showing again.
            onView(withId(R.id.btn_login)).check(matches(isDisplayed()))

            // Step 5: keep a reference to that new Login screen, so we can check it after Back.
            val login = resumedActivity()
            assertTrue("Login should be on screen", login is LoginActivity)

            // Step 6: press Back. "Unconditionally" because leaving the app is what we expect
            // (plain pressBack() would fail the test when the app closes).
            pressBackUnconditionally()

            // Step 7: Login was finished and no earlier screen (Menu, Home) came back,
            // because Log out cleared the back stack.
            assertTrue("Login should be finished", login!!.isFinishing || login.isDestroyed)
            assertTrue("No Kinnect screen should return", resumedActivity() == null)
        }
    }

    /** The app screen currently in the foreground, or null if none (the app has closed). */
    private fun resumedActivity(): Activity? {
        var activity: Activity? = null
        InstrumentationRegistry.getInstrumentation().runOnMainSync {
            activity = ActivityLifecycleMonitorRegistry.getInstance()
                .getActivitiesInStage(Stage.RESUMED).firstOrNull()
        }
        return activity
    }
}
