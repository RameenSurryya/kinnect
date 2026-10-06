package com.rameen.kinnect

import androidx.test.core.app.ActivityScenario
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.Espresso.pressBack
import androidx.test.espresso.action.ViewActions.click
import androidx.test.espresso.action.ViewActions.scrollTo
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.isDisplayed
import androidx.test.espresso.matcher.ViewMatchers.withId
import androidx.test.espresso.matcher.ViewMatchers.withText
import androidx.test.ext.junit.runners.AndroidJUnit4
import com.rameen.kinnect.ui.home.HomeActivity
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Test 1 (multi-step flow): Home -> Comments -> back to Home.
 */
@RunWith(AndroidJUnit4::class)
class HomeToCommentsTest {

    @Test
    fun commentOpensComments_andBackReturnsHome() {
        // Step 1: start the app directly on the Home feed.
        ActivityScenario.launch(HomeActivity::class.java).use {

            // Step 2: Home is showing (the teal "kinnect" wordmark in the top bar).
            onView(withId(R.id.tv_wordmark)).check(matches(isDisplayed()))

            // Step 3: scroll the feed down to the post's Comment button and tap it.
            onView(withId(R.id.ll_comment)).perform(scrollTo(), click())

            // Step 4: the Comments screen opened and its toolbar title reads "Comments".
            onView(withId(R.id.tv_comments_title))
                .check(matches(isDisplayed()))
                .check(matches(withText(R.string.comments_title)))

            // Step 5: press the system Back button.
            pressBack()

            // Step 6: we are back on Home, with the Comment button still there.
            onView(withId(R.id.tv_wordmark)).check(matches(isDisplayed()))
            onView(withId(R.id.ll_comment)).check(matches(isDisplayed()))
        }
    }
}
