package com.rameen.kinnect.ui.social

import android.os.Bundle
import com.rameen.kinnect.R
import com.rameen.kinnect.databinding.ActivityNotificationsBinding
import com.rameen.kinnect.ui.BaseActivity

/**
 * 18 Notifications. UI only: every notification is static sample content.
 *  - Top bar (title, search, messenger) and the tabs are wired by BaseActivity.
 *  - Tapping a notification row opens the other person's profile.
 *  - "...", Confirm, Delete and See previous notifications do nothing.
 */
class NotificationsActivity : BaseActivity() {

    private lateinit var binding: ActivityNotificationsBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityNotificationsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupTopBar(R.string.title_notifications)
        setupTopTabs(Tab.NOTIFICATIONS)

        val rows = listOf(
            binding.llNotifAisha, binding.llNotifSara, binding.llNotifZain,
            binding.llNotifClass, binding.llNotifHamza, binding.llNotifLina,
        )
        for (row in rows) {
            row.setOnClickListener { openScreen("com.rameen.kinnect.ui.profile.OtherProfileActivity") }
        }
    }
}
