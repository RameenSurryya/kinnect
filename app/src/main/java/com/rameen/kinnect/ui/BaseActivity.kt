package com.rameen.kinnect.ui

import android.content.Intent
import android.content.res.ColorStateList
import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.annotation.StringRes
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.widget.ImageViewCompat
import com.rameen.kinnect.R

/**
 * Parent class of every Kinnect screen.
 *
 * It does four shared jobs so each screen stays short:
 *  1. Edge-to-edge system bars, so the screen's own background shows behind the status bar
 *     and the gesture bar (each layout root has android:fitsSystemWindows="true").
 *  2. The five top tabs (layout/include_top_tabs.xml): highlights the active tab and opens
 *     the others with FLAG_ACTIVITY_REORDER_TO_FRONT, so tab screens never pile up.
 *  3. The top bar (layout/include_top_bar.xml): title or wordmark, search and messenger.
 *  4. A one-line helper for back arrows.
 *
 * Usage in a tab screen:
 *   class FriendsActivity : BaseActivity() {
 *       override fun onCreate(savedInstanceState: Bundle?) {
 *           super.onCreate(savedInstanceState)
 *           setContentView(binding.root)
 *           setupTopBar(R.string.title_friends)
 *           setupTopTabs(Tab.FRIENDS)
 *       }
 *   }
 */
abstract class BaseActivity : AppCompatActivity() {

    /** Dark screens (camera, stories, voice call) return true to get white status bar icons. */
    protected open val darkSystemBars: Boolean = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // 1. Transparent status and navigation bars. "dark" = white icons, "light" = dark icons.
        val style = if (darkSystemBars) {
            SystemBarStyle.dark(Color.TRANSPARENT)
        } else {
            SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT)
        }
        enableEdgeToEdge(statusBarStyle = style, navigationBarStyle = style)
    }

    // ---------------------------------------------------------------------------------------
    // 2. Top tabs
    // ---------------------------------------------------------------------------------------

    /**
     * The five tabs. Each one knows its views in include_top_tabs.xml and the screen it opens.
     * Screens are named by class name (text) so this file compiles before they are built;
     * [openScreen] skips any screen that does not exist yet.
     */
    protected enum class Tab(
        val frameId: Int,
        val iconId: Int,
        val indicatorId: Int,
        val screen: String,
    ) {
        HOME(R.id.fl_tab_home, R.id.iv_tab_home, R.id.v_tab_home_indicator,
            "com.rameen.kinnect.ui.home.HomeActivity"),
        FRIENDS(R.id.fl_tab_friends, R.id.iv_tab_friends, R.id.v_tab_friends_indicator,
            "com.rameen.kinnect.ui.social.FriendsActivity"),
        MARKETPLACE(R.id.fl_tab_marketplace, R.id.iv_tab_marketplace, R.id.v_tab_marketplace_indicator,
            "com.rameen.kinnect.ui.market.MarketplaceActivity"),
        NOTIFICATIONS(R.id.fl_tab_notifications, R.id.iv_tab_notifications, R.id.v_tab_notifications_indicator,
            "com.rameen.kinnect.ui.social.NotificationsActivity"),
        MENU(R.id.fl_tab_menu, R.id.iv_tab_menu, R.id.v_tab_menu_indicator,
            "com.rameen.kinnect.ui.social.MenuActivity"),
    }

    /**
     * Highlights [active] (teal icon + teal underline), greys out the others and makes every
     * other tab open its screen. Call after setContentView().
     */
    protected fun setupTopTabs(active: Tab) {
        val teal = ColorStateList.valueOf(ContextCompat.getColor(this, R.color.teal))
        val grey = ColorStateList.valueOf(ContextCompat.getColor(this, R.color.text_grey))

        for (tab in Tab.values()) {
            val isActive = tab == active

            // Icon colour: same as app:tint in the XML, changed from code.
            ImageViewCompat.setImageTintList(findViewById<ImageView>(tab.iconId), if (isActive) teal else grey)

            // Underline: only the active tab shows it (INVISIBLE keeps the layout the same).
            findViewById<View>(tab.indicatorId).visibility = if (isActive) View.VISIBLE else View.INVISIBLE

            val frame = findViewById<View>(tab.frameId)
            frame.isSelected = isActive // TalkBack reads "selected" on the current tab
            frame.setOnClickListener {
                // Tapping the tab you are on does nothing; the others come to the front.
                if (!isActive) openScreen(tab.screen, Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)
            }
        }
    }

    // ---------------------------------------------------------------------------------------
    // 3. Top bar
    // ---------------------------------------------------------------------------------------

    /**
     * Sets the top bar title and wires search and messenger.
     * @param title page title, e.g. R.string.title_friends (Home passes R.string.wordmark)
     * @param wordmark true on Home: shows the title in the teal "kinnect" wordmark style
     */
    protected fun setupTopBar(@StringRes title: Int, wordmark: Boolean = false) {
        val titleView = findViewById<TextView>(R.id.tv_top_title)
        titleView.setText(title)
        if (wordmark) titleView.setTextAppearance(R.style.Kinnect_Text_Wordmark)

        findViewById<View>(R.id.fl_search).setOnClickListener {
            openScreen("com.rameen.kinnect.ui.home.SearchActivity")
        }
        findViewById<View>(R.id.fl_messenger).setOnClickListener {
            openScreen("com.rameen.kinnect.ui.chat.ChatsActivity")
        }
    }

    /** Shows [count] in a red badge, or hides the badge when there is nothing new. */
    protected fun setBadge(badgeId: Int, count: Int) {
        val badge = findViewById<TextView>(badgeId)
        badge.text = count.toString()
        badge.visibility = if (count > 0) View.VISIBLE else View.GONE
    }

    // ---------------------------------------------------------------------------------------
    // 4. Back arrow and navigation
    // ---------------------------------------------------------------------------------------

    /** Makes the view [buttonId] behave like the system Back button (returns to the previous screen). */
    protected fun setupBackButton(buttonId: Int) {
        findViewById<View>(buttonId).setOnClickListener { onBackPressedDispatcher.onBackPressed() }
    }

    /**
     * Opens the screen with the given full class name using an explicit Intent.
     * Until every screen is built some targets do not exist yet: those taps are ignored
     * instead of crashing the app.
     */
    protected fun openScreen(className: String, flags: Int = 0) {
        val intent = Intent().setClassName(this, className).addFlags(flags)
        if (intent.resolveActivity(packageManager) != null) {
            startActivity(intent)
        }
    }
}
