package com.rameen.i230806.ui.social

import android.content.Intent
import android.os.Bundle
import com.rameen.i230806.R
import com.rameen.i230806.databinding.ActivityMenuBinding
import com.rameen.i230806.ui.BaseActivity
import com.rameen.i230806.ui.auth.LoginActivity
import com.rameen.i230806.ui.market.MarketplaceActivity
import com.rameen.i230806.ui.profile.ProfileActivity

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
            openScreen(ProfileActivity::class.java)
        }
        // Friends and Marketplace are tab screens too: bring them to the front, don't stack copies.
        binding.llShortcutFriends.setOnClickListener {
            openScreen(FriendsActivity::class.java, Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)
        }
        binding.llShortcutMarketplace.setOnClickListener {
            openScreen(MarketplaceActivity::class.java, Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)
        }
        // Log out: a new task with everything before it cleared, so Back cannot return here.
        binding.llLogout.setOnClickListener {
            openScreen(
                LoginActivity::class.java,
                Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK,
            )
        }
    }
}
