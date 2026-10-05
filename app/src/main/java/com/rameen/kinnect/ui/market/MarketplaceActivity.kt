package com.rameen.kinnect.ui.market

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityMarketplaceBinding
import com.rameen.kinnect.ui.BaseActivity

/** 23 Marketplace (placeholder until the screen is built). */
class MarketplaceActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityMarketplaceBinding.inflate(layoutInflater).root)
    }
}
