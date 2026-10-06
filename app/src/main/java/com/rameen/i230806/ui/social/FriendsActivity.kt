package com.rameen.i230806.ui.social

import android.os.Bundle
import com.rameen.i230806.R
import com.rameen.i230806.databinding.ActivityFriendsBinding
import com.rameen.i230806.ui.BaseActivity
import com.rameen.i230806.ui.profile.OtherProfileActivity

/**
 * 14 Friends. UI only: the chips and friend requests are static sample content.
 *  - Top bar (title, search, messenger) and the tabs are wired by BaseActivity.
 *  - Tapping a request row opens that person's profile.
 *  - Chips, See all, Confirm and Delete do nothing.
 */
class FriendsActivity : BaseActivity() {

    private lateinit var binding: ActivityFriendsBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityFriendsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupTopBar(R.string.title_friends)
        setupTopTabs(Tab.FRIENDS)

        val requests = listOf(
            binding.llRequestSara, binding.llRequestBilal,
            binding.llRequestNoor, binding.llRequestDaniyal,
        )
        for (row in requests) {
            row.setOnClickListener { openScreen(OtherProfileActivity::class.java) }
        }
    }
}
