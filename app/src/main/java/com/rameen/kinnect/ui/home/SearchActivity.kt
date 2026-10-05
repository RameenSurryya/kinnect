package com.rameen.kinnect.ui.home

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivitySearchBinding
import com.rameen.kinnect.ui.BaseActivity

/** 13 Search (placeholder until the screen is built). */
class SearchActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivitySearchBinding.inflate(layoutInflater).root)
    }
}
