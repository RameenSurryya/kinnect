package com.rameen.i230806.ui.social

import android.os.Bundle
import com.rameen.i230806.R
import com.rameen.i230806.databinding.ActivityNotificationsBinding
import com.rameen.i230806.ui.BaseActivity
import com.rameen.i230806.ui.profile.OtherProfileActivity

/**
 * 18 Notifications. UI only: every notification is static sample content.
 *  - Top bar (title, search, messenger) and the tabs are wired by BaseActivity.
 *  - Tapping the friend request row (Sara Iqbal) opens the other person's profile.
 *  - The other rows, "...", Confirm, Delete and See previous notifications do nothing.
 */
class NotificationsActivity : BaseActivity() {

    private lateinit var binding: ActivityNotificationsBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityNotificationsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupTopBar(R.string.title_notifications)
        setupTopTabs(Tab.NOTIFICATIONS)

        // Only the friend request (Sara Iqbal) leads to another screen: that person's profile.
        binding.llNotifSara.setOnClickListener { openScreen(OtherProfileActivity::class.java) }
    }
}
