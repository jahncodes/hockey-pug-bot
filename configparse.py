import yaml

'''
Loads our configuration file.
'''
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

## Configuration Variables
appName = config['app_name']
botVersion = config['version']
# Discord Application Variables
token = config['discord_app']['token']
prefix = config['discord_app']['prefix']
# Discord Server Specific Variables
serverID = config['discord_server']['server_id']
discussionChannelID = config['discord_server']['discussion_channel']
cmdChannelID = config['discord_server']['cmd_channel']
queueChannelID = config['discord_server']['queue_channel']
draftChannelID = config['discord_server']['draft_channel']
matchChannelID = config['discord_server']['match_channel']
resultChannelID = config['discord_server']['result_channel']
lbChannelID = config['discord_server']['lb_channel']
logChannelID = config['discord_server']['log_channel']
categoryID = config['discord_server']['category_id']
notificationRoleID = config['discord_server']['notification_role']
modID = config['staff_roles']['level1_id']
adminID = config['staff_roles']['level2_id']
allAccessID = config['staff_roles']['level3_id']
# Promotion/Demotion Variables
startingSkillRating = config['promotion_demotion']['starting_skill_rating']
promotionEnabled = config['promotion_demotion']['promotion_enabled']
skillRatingPromotion = config['promotion_demotion']['skill_rating_promotion']
promotionRoleID = config['promotion_demotion']['promotion_role_id']
demotionEnabled = config['promotion_demotion']['demotion_enabled']
skillRatingDemotion = config['promotion_demotion']['skill_rating_demotion']
demotionRoleID = config['promotion_demotion']['demotion_role_id']
# Season Variables
activeSeason = config['seasons']['active_season']
# Custom Bot Variables
playerCount = config['settings']['player_count']
buttonCooldown = config['settings']['button_cooldown']
queueInactivity = config['settings']['queue_inactivity']
matchInactivity = config['settings']['match_inactivity']
captainNotiInterval = config['settings']['captain_noti_interval']
captainInactivity = config['settings']['captain_inactivity']
queueNotification = config['settings']['queue_notification']
# Database Variables
dbName = config['database']['db_name']
# Hockey API Variables
environment = config['slapshot']['environment']
apiKey = config['slapshot']['api_key']
apiRate = config['slapshot']['api_rate']
region = config['slapshot']['region']
arena = config['slapshot']['arena']
gamemode = config['slapshot']['gamemode']
lobbyName = config['slapshot']['lobby_name']
creatorName = config['slapshot']['creater_name']
periods = config['slapshot']['periods']
mercyRule = config['slapshot']['mercy_rule']
matchLength = config['slapshot']['match_length']
teamSizeLimit = config['slapshot']['team_size_limit']
homeStartingScore = config['slapshot']['home_starting_score']
awayStartingScore = config['slapshot']['away_starting_score']
# Discord Embed Variables
thumbnail = config['discord_embed']['thumbnail']
embedTheme = config['discord_embed']['embed_theme']
footer = config['discord_embed']['footer']
footerIcon = config['discord_embed']['footer_icon']
queueTitle = config['discord_embed']['queue_title']
typePrefix = config['discord_embed']['type_prefix']
emojiRed = config['discord_embed']['emoji_red']
emojiGreen = config['discord_embed']['emoji_green']
emojiSuccess = config['discord_embed']['emoji_success']
emojiCancel = config['discord_embed']['emoji_cancel']
greenColor = config['discord_embed']['green_color']
redColor = config['discord_embed']['red_color']
defaultPicture = config['discord_embed']['profile_icon']