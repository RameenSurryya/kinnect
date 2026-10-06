package com.rameen.kinnect.ui.market

import android.os.Bundle
import com.rameen.kinnect.R
import com.rameen.kinnect.databinding.ActivityMarketplaceBinding
import com.rameen.kinnect.ui.BaseActivity

/**
 * 23 Marketplace. UI only: the pills and products are static sample content.
 *  - Top bar (title, search, messenger) and the tabs are wired by BaseActivity.
 *  - Sell, Categories and the product cards do nothing.
 */
class MarketplaceActivity : BaseActivity() {

    private lateinit var binding: ActivityMarketplaceBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMarketplaceBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupTopBar(R.string.title_marketplace)
        setupTopTabs(Tab.MARKETPLACE)

        // Cuts each photo to its 12dp rounded corners (bg_photo_rounded);
        // XML only has this attribute from Android 12.
        binding.ivProductBike.clipToOutline = true
        binding.ivProductChair.clipToOutline = true
        binding.ivProductDesk.clipToOutline = true
        binding.ivProductPots.clipToOutline = true
    }
}
