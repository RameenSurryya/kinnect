package com.rameen.i230806.ui.home

import android.os.Bundle
import com.rameen.i230806.R
import com.rameen.i230806.databinding.ActivitySearchBinding
import com.rameen.i230806.ui.BaseActivity
import com.rameen.i230806.ui.profile.OtherProfileActivity

/**
 * 13 Search. UI only: the query "omar", the chips and every result are static sample content.
 * The back arrow (and system Back) returns to Home; tapping a person row opens their profile.
 * Chips, clear, add friend, See all people, Join and the recent-search X are visual only.
 */
class SearchActivity : BaseActivity() {

    private lateinit var binding: ActivitySearchBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivitySearchBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupBackButton(R.id.iv_back)

        // The three person rows all open the other person's profile.
        for (row in listOf(binding.llPersonOmarF, binding.llPersonOmarS, binding.llPersonOmarT)) {
            row.setOnClickListener { openScreen(OtherProfileActivity::class.java) }
        }
    }
}
