\# Screens (Activity / layout / package)

Tabs = shows the shared top tab bar (include\_top\_tabs).



| # | Activity | Package | Tabs | Goes to |

|---|----------|---------|------|---------|

| 01 | SplashActivity | auth | no | Login after \~2 s, finish() |

| 02 | LoginActivity | auth | no | Log in → Home (finish); Create new account → SignUp |

| 03 | SignUpActivity | auth | no | Create account → Home; "Log in" → Login; back arrow → back |

| 04 | HomeActivity | home | yes | search → Search; messenger → Chats; composer → CreatePost; Comment → Comments; long-press Like → ReactionPicker; story card → StoryViewer; Create story → Camera; avatar → Profile |

| 05 | ReactionPickerActivity | home | no | back → Home |

| 06 | CommentsActivity | home | no | back → Home |

| 07 | CreatePostActivity | home | no | Photo/video → PhotoPicker; Camera → Camera; X / back → back |

| 08 | PhotoPickerActivity | home | no | Next → CreatePost; Cancel → back |

| 09 | CameraActivity | home | no | shutter → StoryEditor; X → back |

| 10 | StoryEditorActivity | home | no | arrow / Your story → YourStory; X → back |

| 11 | StoryViewerActivity | home | no | X → back |

| 12 | YourStoryActivity | home | no | X → Home |

| 13 | SearchActivity | home | no | person result → OtherProfile; back |

| 14 | FriendsActivity | social | yes | request tap → OtherProfile |

| 15 | ProfileActivity | profile | no | Edit profile → EditProfile; back |

| 16 | EditProfileActivity | profile | no | Save / Cancel → Profile |

| 17 | OtherProfileActivity | profile | no | Message → Chat; back |

| 18 | NotificationsActivity | social | yes | friend request name → OtherProfile |

| 19 | MenuActivity | social | yes | profile card → Profile; Friends / Marketplace shortcuts; Log out → Login (clear stack) |

| 20 | ChatsActivity | chat | no | row → Chat; back |

| 21 | ChatActivity | chat | no | phone icon → VoiceCall; back |

| 22 | VoiceCallActivity | chat | no | end call → back to Chat |

| 23 | MarketplaceActivity | market | yes | tabs only |

