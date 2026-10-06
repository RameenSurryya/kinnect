package com.rameen.kinnect.ui.social

import android.content.Intent
import android.os.Bundle
import com.rameen.kinnect.R
import com.rameen.kinnect.databinding.ActivityMenuBinding
import com.rameen.kinnect.ui.BaseActivity

/**
 * 19 Menu. UI only: the shortcuts and rows are static sample content.
 *  - Top bar (title, search, messenger) and the tabs are wired by BaseActivity.
 *  - Profile card opens Profile; the Friends and Marketplace shortcuts open those screens.
 *  - Log out opens Login and clears the back stack, so Back leaves the app.
 *  - Memories, Saved, Groups, Events, See more and the three rows do nothing.
 */
class MenuActivity : BaseActivity() {

    private lateinit var binding: ActivityMenuBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMenuBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupTopBar(R.string.title_menu)
        setupTopTabs(Tab.MENU)

        binding.llProfileCard.setOnClickListener {
            openScreen("com.rameen.kinnect.ui.profile.ProfileActivity")
        }
        // Friends and Marketplace are tab screens too: bring them to the front, don't stack copies.
        binding.llShortcutFriends.setOnClickListener {
            openScreen("com.rameen.kinnect.ui.social.FriendsActivity", Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)
        }
        binding.llShortcutMarketplace.setOnClickListener {
            openScreen("com.rameen.kinnect.ui.market.MarketplaceActivity", Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)
        }
        // Log out: a new task with everything before it cleared, so Back cannot return here.
        binding.llLogout.setOnClickListener {
            openScreen(
                "com.rameen.kinnect.ui.auth.LoginActivity",
                Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK,
            )
        }
    }
}
