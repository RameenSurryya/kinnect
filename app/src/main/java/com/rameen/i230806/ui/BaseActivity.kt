package com.rameen.i230806.ui

import android.app.Activity
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
import com.rameen.i230806.R
import com.rameen.i230806.ui.chat.ChatsActivity
import com.rameen.i230806.ui.home.HomeActivity
import com.rameen.i230806.ui.home.SearchActivity
import com.rameen.i230806.ui.market.MarketplaceActivity
import com.rameen.i230806.ui.social.FriendsActivity
import com.rameen.i230806.ui.social.MenuActivity
import com.rameen.i230806.ui.social.NotificationsActivity

/**
 * Parent class of every Kinnect screen.
 *
 * It does four shared jobs so each screen stays short:
 *  1. Edge-to-edge system bars, so the screen's own background shows behind the status bar
 *     and the gesture bar (each layout root has android:fitsSystemWindows="true").
 *  2. The five top tabs (layout/include_top_tabs.xml): highlights the active tab and opens
 *     the others with FLAG_ACTIVITY_REORDER_TO_FRONT, so tab screens never pile up.
 *  3. The top bar (layout/include_top_bar.xml): page title (or the wordmark on Home via
 *     setupHomeTopBar()), search and messenger.
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
     */
    protected enum class Tab(
        val frameId: Int,
        val iconId: Int,
        val indicatorId: Int,
        val screen: Class<out Activity>,
    ) {
        HOME(R.id.fl_tab_home, R.id.iv_tab_home, R.id.v_tab_home_indicator,
            HomeActivity::class.java),
        FRIENDS(R.id.fl_tab_friends, R.id.iv_tab_friends, R.id.v_tab_friends_indicator,
            FriendsActivity::class.java),
        MARKETPLACE(R.id.fl_tab_marketplace, R.id.iv_tab_marketplace, R.id.v_tab_marketplace_indicator,
            MarketplaceActivity::class.java),
        NOTIFICATIONS(R.id.fl_tab_notifications, R.id.iv_tab_notifications, R.id.v_tab_notifications_indicator,
            NotificationsActivity::class.java),
        MENU(R.id.fl_tab_menu, R.id.iv_tab_menu, R.id.v_tab_menu_indicator,
            MenuActivity::class.java),
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

    /** Tab screens: shows the page title, e.g. setupTopBar(R.string.title_friends). */
    protected fun setupTopBar(@StringRes title: Int) {
        findViewById<TextView>(R.id.tv_top_title).setText(title)
        wireTopBarButtons()
    }

    /** Home: shows the teal "kinnect" wordmark instead of a page title. */
    protected fun setupHomeTopBar() {
        findViewById<View>(R.id.tv_top_title).visibility = View.GONE
        findViewById<View>(R.id.tv_wordmark).visibility = View.VISIBLE
        wireTopBarButtons()
    }

    /** Search opens the Search screen, messenger opens the Chats list. */
    private fun wireTopBarButtons() {
        findViewById<View>(R.id.fl_search).setOnClickListener {
            openScreen(SearchActivity::class.java)
        }
        findViewById<View>(R.id.fl_messenger).setOnClickListener {
            openScreen(ChatsActivity::class.java)
        }
    }

    // ---------------------------------------------------------------------------------------
    // 4. Back arrow and navigation
    // ---------------------------------------------------------------------------------------

    /** Makes the view [buttonId] (back arrow, X, Cancel) close this screen and return to the previous one. */
    protected fun setupBackButton(buttonId: Int) {
        findViewById<View>(buttonId).setOnClickListener { finish() }
    }

    /** Opens [screen] with an explicit Intent, plus optional flags (e.g. REORDER_TO_FRONT for tabs). */
    protected fun openScreen(screen: Class<out Activity>, flags: Int = 0) {
        startActivity(Intent(this, screen).addFlags(flags))
    }
}
