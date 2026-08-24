import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ApplicationWindow {
    id: root
    visible: true
    width: 1500
    height: 920
    minimumWidth: 1120
    minimumHeight: 720
    title: "ARLEN NEXUS — Personal Intelligence & System Control Environment"
    color: theme.bg
    flags: Qt.Window | Qt.FramelessWindowHint

    property int activePage: 0
    property bool openingVisible: true
    property bool dataFlow: backend.networkStatus === "Online"
    property var theme: themePalette(backend.currentTheme)
    property real flowTick: 0
    property double clockTick: Date.now()

    Timer { interval: 45; running: root.dataFlow; repeat: true; onTriggered: root.flowTick += 5 }
    Timer { interval: 1000; running: true; repeat: true; onTriggered: root.clockTick = Date.now() }

    function themePalette(name) {
        if (name === "Crimson") return {bg:"#070407", panel:"#11080d", card:"#190d14", line:"#4b1a2b", text:"#f5eef1", muted:"#9c7885", accent:"#e43f68", good:"#63d89b", warn:"#d8a84d"}
        if (name === "Emerald") return {bg:"#030806", panel:"#07130e", card:"#0a1d15", line:"#164b34", text:"#e9fff5", muted:"#6c9a84", accent:"#32df91", good:"#63eba8", warn:"#d2ae53"}
        if (name === "Violet") return {bg:"#06050a", panel:"#0e0b17", card:"#171125", line:"#39285d", text:"#f2effb", muted:"#8c83a7", accent:"#9d72f2", good:"#62d5a1", warn:"#d6ac54"}
        if (name === "Arctic") return {bg:"#e8f0f3", panel:"#f7fbfc", card:"#dce9ed", line:"#a9c4cd", text:"#12252d", muted:"#5e7780", accent:"#087f9e", good:"#087e5b", warn:"#996d13"}
        return {bg:"#02070c", panel:"#06121b", card:"#091a26", line:"#133c50", text:"#e8f8fc", muted:"#6f909f", accent:"#28cce8", good:"#53d99a", warn:"#d5a449"}
    }

    component AppButton: Button {
        id: control
        property bool selected: false
        implicitHeight: 46
        background: Rectangle { radius: 8; color: control.selected ? Qt.rgba(0.1,0.55,0.68,0.18) : (control.hovered ? theme.card : "transparent"); border.color: control.selected ? theme.accent : "transparent" }
        contentItem: Text { text: control.text; color: control.selected ? theme.accent : theme.text; font.pixelSize: 13; font.weight: Font.Medium; verticalAlignment: Text.AlignVCenter; leftPadding: 14 }
    }

    component Panel: Rectangle {
        color: theme.panel
        radius: 12
        border.color: theme.line
        border.width: 1
    }

    component Metric: Rectangle {
        property string label: "METRIC"
        property string value: "0%"
        property real progress: 0
        color: theme.card
        radius: 9
        implicitHeight: 74
        Column { anchors.fill: parent; anchors.margins: 12; spacing: 7
            Row { width: parent.width; Text { text: label; color: theme.muted; font.pixelSize: 11; width: parent.width-55 } Text { text: value; color: theme.text; font.pixelSize: 14; font.weight: Font.Medium } }
            Rectangle { width: parent.width; height: 3; radius: 2; color: theme.line
                Rectangle { width: parent.width*Math.max(0,Math.min(1,progress)); height: parent.height; radius: 2; color: progress > .85 ? "#d95b5b" : theme.accent; Behavior on width { NumberAnimation { duration: 400 } } }
            }
        }
    }

    component PageTitle: Row {
        property alias title: titleText.text
        property alias subtitle: subText.text
        spacing: 14
        Text { id: titleText; color: theme.text; font.pixelSize: 23; font.weight: Font.Medium }
        Text { id: subText; color: theme.muted; font.pixelSize: 12; anchors.baseline: titleText.baseline }
    }

    Rectangle {
        id: topbar
        anchors.left: parent.left; anchors.right: parent.right; anchors.top: parent.top
        height: 72; color: theme.bg; border.color: theme.line
        MouseArea { anchors.fill: parent; acceptedButtons: Qt.LeftButton; onPressed: root.startSystemMove() }
        Row { anchors.left: parent.left; anchors.leftMargin: 24; anchors.verticalCenter: parent.verticalCenter; spacing: 12
            Rectangle { width: 38; height: 38; radius: 19; color: "transparent"; border.color: theme.accent; Text { anchors.centerIn: parent; text: "A"; color: theme.accent; font.pixelSize: 19; font.weight: Font.DemiBold } }
            Column { spacing: 1
                Text { text: "ARLEN NEXUS"; color: theme.text; font.pixelSize: 19; font.weight: Font.DemiBold }
                Text { text: "PERSONAL INTELLIGENCE & SYSTEM CONTROL ENVIRONMENT"; color: theme.muted; font.pixelSize: 9 }
            }
        }
        Row { anchors.centerIn: parent; spacing: 30
            Column { Text { text: Qt.formatDateTime(new Date(root.clockTick), "hh:mm:ss AP"); color: theme.text; font.pixelSize: 17 } Text { text: Qt.formatDateTime(new Date(root.clockTick), "dddd, dd MMMM yyyy"); color: theme.muted; font.pixelSize: 10 } }
            Column { Text { text: "●  " + backend.networkStatus.toUpperCase(); color: backend.networkStatus === "Online" ? theme.good : theme.warn; font.pixelSize: 12; font.weight: Font.DemiBold } Text { text: "PRIVATE LOCAL SESSION"; color: theme.muted; font.pixelSize: 9 } }
        }
        Row { anchors.right: windowButtons.left; anchors.rightMargin: 24; anchors.verticalCenter: parent.verticalCenter; spacing: 8
            Text { text: backend.ownerName.toUpperCase(); color: theme.text; font.pixelSize: 12 }
            Rectangle { width: 34; height: 34; radius: 17; color: theme.card; border.color: theme.accent; clip:true
                Image { anchors.fill:parent; source:backend.ownerAvatar; fillMode:Image.PreserveAspectCrop; visible:backend.ownerAvatar.length>0 }
                Text { anchors.centerIn: parent; visible:backend.ownerAvatar.length===0; text: backend.ownerName.split(" ").map(function(v){return v.charAt(0)}).join("").slice(0,2).toUpperCase(); color: theme.accent; font.pixelSize: 11 }
            }
        }
        Row { id: windowButtons; anchors.right: parent.right; anchors.verticalCenter: parent.verticalCenter; spacing: 0
            Repeater { model: ["—","□","×"]
                Button { required property string modelData; text: modelData; width: 45; height: 40
                    background: Rectangle { color: parent.hovered ? (modelData === "×" ? "#752633" : theme.card) : "transparent" }
                    contentItem: Text { text: parent.text; color: theme.text; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                    onClicked: modelData === "×" ? Qt.quit() : (modelData === "—" ? root.showMinimized() : (root.visibility === Window.Maximized ? root.showNormal() : root.showMaximized()))
                }
            }
        }
    }

    Rectangle {
        id: sidebar
        anchors.top: topbar.bottom; anchors.bottom: parent.bottom; anchors.left: parent.left
        width: 210; color: theme.panel; border.color: theme.line
        Column { anchors.fill: parent; anchors.margins: 12; spacing: 3
            Repeater { model: ["⌂   HOME","◈   CHAT","◉   VOICE","▣   SYSTEM","⌁   NETWORK","▤   FILES","↻   AUTOMATION","◇   CLEANUP","⬡   SECURITY","⚙   ADMIN","▧   IMAGE STUDIO","◉   VISION / OCR","▤   PDF STUDIO","✦   THEME STUDIO","ⓘ   ABOUT"]
                AppButton { required property string modelData; required property int index; width: parent.width; text: modelData; selected: root.activePage === index; onClicked: root.activePage = index }
            }
            Item { width: 1; height: 14 }
            Rectangle { width: parent.width; height: 1; color: theme.line }
            Text { text: "GLOBAL ACCESS"; color: theme.muted; font.pixelSize: 9; leftPadding: 14; topPadding: 12 }
            Text { text: "CTRL + ALT + A"; color: theme.accent; font.pixelSize: 12; leftPadding: 14; topPadding: 6 }
            Text { text: "CORE STATUS  ● READY"; color: theme.good; font.pixelSize: 10; leftPadding: 14; topPadding: 12 }
        }
    }

    StackLayout {
        anchors.top: topbar.bottom; anchors.bottom: parent.bottom; anchors.left: sidebar.right; anchors.right: parent.right
        currentIndex: root.activePage

        Item { // HOME
            anchors.margins: 18
            RowLayout { anchors.fill: parent; spacing: 14
                ColumnLayout { Layout.preferredWidth: 260; Layout.fillHeight: true; spacing: 12
                    Panel { Layout.fillWidth: true; Layout.fillHeight: true
                        Column { anchors.fill: parent; anchors.margins: 14; spacing: 9
                            Text { text: "SYSTEM OVERVIEW"; color: theme.text; font.pixelSize: 12; font.weight: Font.DemiBold }
                            Metric { width: parent.width; label: "CPU USAGE"; value: backend.cpu.toFixed(0)+"%"; progress: backend.cpu/100 }
                            Metric { width: parent.width; label: "RAM USAGE"; value: backend.ram.toFixed(0)+"%"; progress: backend.ram/100 }
                            Metric { width: parent.width; label: "DISK USAGE"; value: backend.disk.toFixed(0)+"%"; progress: backend.disk/100 }
                            Text { text: "UPTIME\n"+backend.uptime; color: theme.muted; font.pixelSize: 11; lineHeight: 1.35 }
                        }
                    }
                    Panel { Layout.fillWidth: true; Layout.preferredHeight: 200
                        Column { anchors.fill: parent; anchors.margins: 14; spacing: 10
                            Text { text: "TOP MEMORY PROCESSES"; color: theme.text; font.pixelSize: 12; font.weight: Font.DemiBold }
                            Text { text: backend.topApps; color: theme.muted; font.pixelSize: 11; lineHeight: 1.55 }
                        }
                    }
                }

                ColumnLayout { Layout.fillWidth: true; Layout.fillHeight: true; spacing: 12
                    Panel { Layout.fillWidth: true; Layout.fillHeight: true
                        Item { anchors.fill: parent
                            Image { id: sphere; anchors.centerIn: parent; width: Math.min(parent.width*.63, parent.height*.82); height: width; source: backend.customSphere.length ? backend.customSphere : "../assets/neural-sphere.png"; fillMode: Image.PreserveAspectFit; opacity: .87
                                RotationAnimator on rotation { from: 0; to: 360; duration: 65000; loops: Animation.Infinite }
                            }
                            Rectangle { anchors.centerIn: sphere; width: sphere.width*.34; height: width; radius: width/2; color: "transparent"; border.color: theme.accent; border.width: 1; opacity: .55
                                SequentialAnimation on scale { loops: Animation.Infinite; NumberAnimation { to:1.08; duration:1200; easing.type:Easing.InOutSine } NumberAnimation { to:1; duration:1200; easing.type:Easing.InOutSine } }
                            }
                            Repeater { model: 54
                                Text { required property int index; visible: root.dataFlow; text: index%3 ? "0" : "1"; color: index%4 ? theme.good : "#cf5864"; opacity: .5; font.family: "Consolas"; font.pixelSize: 9; x: (index*97 + root.flowTick) % Math.max(1,parent.width); y: (index*53 + root.flowTick*(index%2 ? .2 : -.2) + parent.height) % Math.max(1,parent.height) }
                            }
                            Column { anchors.horizontalCenter: parent.horizontalCenter; anchors.bottom: parent.bottom; anchors.bottomMargin: 22; spacing: 4
                                Text { anchors.horizontalCenter: parent.horizontalCenter; text: "ARLEN CORE"; color: theme.text; font.pixelSize: 16; font.weight: Font.Medium }
                                Text { anchors.horizontalCenter: parent.horizontalCenter; text: root.dataFlow ? "DATA FLOW ACTIVE" : "LOCAL CORE READY"; color: root.dataFlow ? theme.good : theme.accent; font.pixelSize: 10 }
                            }
                        }
                    }
                    Panel { Layout.fillWidth: true; Layout.preferredHeight: 82
                        RowLayout { anchors.fill: parent; anchors.margins: 12; spacing: 10
                            TextField { id: quickInput; Layout.fillWidth: true; placeholderText: "Message or command ARLEN…"; color: theme.text; placeholderTextColor: theme.muted; background: Rectangle { color: theme.card; radius: 8; border.color: theme.line } onAccepted: { backend.execute(text); text="" } }
                            Button { text: "EXECUTE"; onClicked: { backend.execute(quickInput.text); quickInput.text="" } background: Rectangle { color: theme.accent; radius: 8 } contentItem: Text { text: parent.text; color: "#021014"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter; font.weight: Font.DemiBold } }
                        }
                    }
                }

                ColumnLayout { Layout.preferredWidth: 270; Layout.fillHeight: true; spacing: 12
                    Panel { Layout.fillWidth: true; Layout.preferredHeight: 225
                        Column { anchors.fill: parent; anchors.margins: 14; spacing: 10
                            Text { text: "NETWORK STATUS"; color: theme.text; font.pixelSize: 12; font.weight: Font.DemiBold }
                            Text { text: "WI-FI\n"+backend.wifiName; color: theme.muted; font.pixelSize: 11; lineHeight: 1.3 }
                            Text { text: "DOWNLOAD   "+backend.downloadSpeed.toFixed(2)+" Mbps"; color: theme.good; font.pixelSize: 12 }
                            Text { text: "UPLOAD       "+backend.uploadSpeed.toFixed(2)+" Mbps"; color: "#cf6973"; font.pixelSize: 12 }
                            Text { text: backend.sessionUsage(); color: theme.muted; font.pixelSize: 10 }
                        }
                    }
                    Panel { Layout.fillWidth: true; Layout.preferredHeight: 205
                        Column { anchors.fill: parent; anchors.margins: 14; spacing: 12
                            Text { text: "SECURITY CENTER"; color: theme.text; font.pixelSize: 12; font.weight: Font.DemiBold }
                            Text { text: "●  FIREWALL MONITORED\n●  LOCAL BRAIN PRIVATE\n●  BRAVE SHIELD AVAILABLE\n●  ADMIN CONTROL ACTIVE"; color: theme.good; font.pixelSize: 10; lineHeight: 1.65 }
                            AppButton { width: parent.width; text: "OPEN SECURITY HUB"; onClicked: root.activePage=8 }
                        }
                    }
                    Panel { Layout.fillWidth: true; Layout.fillHeight: true
                        Column { anchors.fill: parent; anchors.margins: 14; spacing: 8
                            Text { text: "QUICK COMMANDS"; color: theme.text; font.pixelSize: 12; font.weight: Font.DemiBold }
                            Repeater { model: ["Open Brave","Open Downloads","Show system status","Cleanup system","Take screenshot"]
                                AppButton { required property string modelData; width: parent.width; text: modelData; onClicked: backend.execute(modelData) }
                            }
                        }
                    }
                }
            }
        }

        Item { // CHAT
            ColumnLayout { anchors.fill: parent; anchors.margins: 22; spacing: 12
                PageTitle { title: "CONVERSATIONAL BRAIN"; subtitle: "PRIVATE • LOCAL MODEL • NO CLOUD" }
                Panel { Layout.fillWidth: true; Layout.fillHeight: true
                    ListView { id: chatList; anchors.fill: parent; anchors.margins: 18; spacing: 12; clip: true; model: ListModel { id: chatModel }
                        delegate: Rectangle { required property string role; required property string body; width: Math.min(chatList.width*.75, bodyText.implicitWidth+38); height: bodyText.implicitHeight+28; radius: 10; color: role === "YOU" ? Qt.rgba(.12,.5,.8,.18) : theme.card; border.color: role === "YOU" ? theme.accent : theme.line; x: role === "YOU" ? chatList.width-width : 0
                            Text { id: bodyText; anchors.fill: parent; anchors.margins: 14; text: parent.body; color: theme.text; wrapMode: Text.Wrap; font.pixelSize: 13 }
                        }
                    }
                }
                RowLayout { Layout.fillWidth: true
                    TextField { id: chatInput; Layout.fillWidth: true; placeholderText: "Write to ARLEN…"; color: theme.text; placeholderTextColor: theme.muted; background: Rectangle { color: theme.panel; radius: 9; border.color: theme.line } onAccepted: sendChat() }
                    Button { text: "SEND"; onClicked: sendChat(); background: Rectangle { color: theme.accent; radius: 8 } }
                    Button { text: "UNLOAD BRAIN"; onClicked: backend.unloadBrain(); background: Rectangle { color: theme.card; radius: 8; border.color: theme.line } contentItem: Text { text: parent.text; color: theme.text; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter } }
                }
            }
            function sendChat() { if(chatInput.text.trim().length){ chatModel.append({role:"YOU",body:chatInput.text}); backend.sendChat(chatInput.text); chatInput.text="" } }
            Connections { target: backend; function onChatReply(reply, state){ chatModel.append({role:"ARLEN",body:reply}); chatList.positionViewAtEnd() } }
        }

        Item { // VOICE
            ColumnLayout { anchors.fill: parent; anchors.margins: 24; spacing: 16
                PageTitle { title: "VOICE CONTROL"; subtitle: "PUSH-TO-TALK • OFFLINE RECOGNITION" }
                Panel { Layout.fillWidth: true; Layout.fillHeight: true
                    Column { anchors.centerIn: parent; width:620; spacing: 16
                        Rectangle { anchors.horizontalCenter: parent.horizontalCenter; width: 210; height: 210; radius: 105; color: theme.card; border.color: theme.accent; border.width: 2
                            Text { anchors.centerIn: parent; text: "◉"; color: theme.accent; font.pixelSize: 70 }
                            SequentialAnimation on scale { loops: Animation.Infinite; NumberAnimation { to:1.04; duration:1000 } NumberAnimation { to:1; duration:1000 } }
                        }
                        Text { id: voiceStatus; anchors.horizontalCenter: parent.horizontalCenter; text: "VOICE PACK STANDBY"; color: theme.text; font.pixelSize: 18 }
                        AppButton { width: 260; text: "START LISTENING"; onClicked: backend.startVoice() }
                        TextField { id:heardCommand; width:parent.width; placeholderText:"Voice interpretation test: Brave kholo / open calculator"; color:theme.text; placeholderTextColor:theme.muted; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} onAccepted:backend.interpretVoiceText(text) }
                        Row { anchors.horizontalCenter:parent.horizontalCenter; spacing:10
                            TextField { id:wakeWordField; width:190; text:backend.wakeWord; placeholderText:"Wake word"; color:theme.text; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                            ComboBox { id:voiceLanguage; width:180; model:["Auto Detect","Bangla","Banglish","English"] }
                            AppButton { width:190; text:"SAVE VOICE PROFILE"; onClicked:backend.saveVoicePreferences(wakeWordField.text,voiceLanguage.currentText) }
                        }
                        Text { width: 520; horizontalAlignment: Text.AlignHCenter; wrapMode: Text.Wrap; text: "The microphone activates only when you press the button or use the configured shortcut. Audio remains on this PC."; color: theme.muted; font.pixelSize: 11 }
                    }
                }
            }
            Connections { target: backend; function onVoiceStateChanged(state){ voiceStatus.text=state } }
        }

        Item { // SYSTEM
            ColumnLayout { anchors.fill: parent; anchors.margins: 22; spacing: 14
                PageTitle { title: "SYSTEM CONTROL"; subtitle: "LIVE PERFORMANCE & PROCESS MANAGEMENT" }
                GridLayout { Layout.fillWidth: true; columns: 3; columnSpacing: 12
                    Metric { Layout.fillWidth: true; label:"CPU"; value:backend.cpu.toFixed(0)+"%"; progress:backend.cpu/100 }
                    Metric { Layout.fillWidth: true; label:"MEMORY"; value:backend.ram.toFixed(0)+"%"; progress:backend.ram/100 }
                    Metric { Layout.fillWidth: true; label:"SYSTEM DISK"; value:backend.disk.toFixed(0)+"%"; progress:backend.disk/100 }
                }
                Panel { Layout.fillWidth: true; Layout.fillHeight: true
                    Column { anchors.fill: parent; anchors.margins: 18; spacing: 12
                        Text { text:"TOP MEMORY PROCESSES"; color:theme.accent; font.pixelSize:12 }
                        Text { text:backend.topApps; color:theme.text; font.pixelSize:14; lineHeight:1.7 }
                        AppButton { width:240; text:"OPEN TASK MANAGER"; onClicked:backend.execute("open task manager") }
                    }
                }
            }
        }

        Item { // NETWORK
            ColumnLayout { anchors.fill: parent; anchors.margins: 22; spacing: 14
                PageTitle { title:"NETWORK MATRIX"; subtitle:"LIVE WI-FI SPEED & SESSION USAGE" }
                RowLayout { Layout.fillWidth:true; spacing:12
                    Metric { Layout.fillWidth:true; label:"DOWNLOAD SPEED"; value:backend.downloadSpeed.toFixed(2)+" Mbps"; progress:Math.min(1,backend.downloadSpeed/100) }
                    Metric { Layout.fillWidth:true; label:"UPLOAD SPEED"; value:backend.uploadSpeed.toFixed(2)+" Mbps"; progress:Math.min(1,backend.uploadSpeed/50) }
                    Metric { Layout.fillWidth:true; label:"CONNECTION"; value:backend.networkStatus; progress:backend.networkStatus==="Online"?1:0 }
                }
                Panel { Layout.fillWidth:true; Layout.fillHeight:true
                    Column { anchors.centerIn:parent; spacing:18
                        Text { anchors.horizontalCenter:parent.horizontalCenter; text:"WI-FI  •  "+backend.wifiName; color:theme.text; font.pixelSize:20 }
                        Text { anchors.horizontalCenter:parent.horizontalCenter; text:backend.sessionUsage(); color:theme.accent; font.pixelSize:16 }
                        Text { width:600; wrapMode:Text.Wrap; horizontalAlignment:Text.AlignHCenter; text:"Data flow animation appears around the neural core only while network traffic or command processing is active. Visual opacity is limited to 50% by default."; color:theme.muted; font.pixelSize:12 }
                    }
                }
            }
        }

        Item { // FILES
            ColumnLayout { anchors.fill:parent; anchors.margins:22; spacing:14
                PageTitle { title:"FILE INTELLIGENCE"; subtitle:"SEARCH • ORGANIZE • CONTROLLED MODIFICATION" }
                Panel { Layout.fillWidth:true; Layout.fillHeight:true
                    Column { anchors.fill:parent; anchors.margins:20; spacing:12
                        TextField { width:parent.width; placeholderText:"Search files by name…"; color:theme.text; placeholderTextColor:theme.muted; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                        Text { text:"Quick locations"; color:theme.accent; font.pixelSize:12 }
                        Row { spacing:10; Repeater { model:["Downloads","Documents","Desktop","Pictures"]; delegate: AppButton { required property string modelData; width:150; text:modelData; onClicked:backend.execute("open "+modelData) } } }
                        Text { text:"File modification, move, rename and deletion use preview + confirmation. Protected locations require Admin authorization."; color:theme.muted; font.pixelSize:11; wrapMode:Text.Wrap; width:parent.width }
                    }
                }
            }
        }

        Item { // AUTOMATION
            ColumnLayout { anchors.fill:parent; anchors.margins:22; spacing:14
                PageTitle { title:"AUTOMATION LAB"; subtitle:"CUSTOM COMMANDS • MACROS • SCHEDULES" }
                RowLayout { Layout.fillWidth:true; Layout.fillHeight:true; spacing:14
                    Panel { Layout.fillWidth:true; Layout.fillHeight:true
                        Column { anchors.fill:parent; anchors.margins:20; spacing:12
                            Text { text:"TEACH ARLEN A COMMAND"; color:theme.accent; font.pixelSize:12 }
                            TextField { id:macroTrigger; width:parent.width; placeholderText:"Trigger: Start Work Mode"; color:theme.text; placeholderTextColor:theme.muted; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                            TextArea { id:macroActions; width:parent.width; height:120; placeholderText:"Actions, one per line:\nopen brave\nopen vs code\nopen documents"; color:theme.text; placeholderTextColor:theme.muted; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                            TextField { id:macroResponse; width:parent.width; placeholderText:"Voice/text response: Work environment ready."; color:theme.text; placeholderTextColor:theme.muted; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                            TextField { id:macroPin; width:220; echoMode:TextInput.Password; placeholderText:"Owner PIN"; color:theme.text; placeholderTextColor:theme.muted; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                            AppButton { width:260; text:"SAVE CUSTOM COMMAND"; onClicked:backend.addCustomCommand(macroTrigger.text,macroActions.text,macroResponse.text,macroPin.text) }
                            Text { width:parent.width; wrapMode:Text.Wrap; text:"Power, delete and protected actions cannot be hidden inside a macro. They always request confirmation."; color:theme.muted; font.pixelSize:10 }
                        }
                    }
                    Panel { Layout.preferredWidth:430; Layout.fillHeight:true
                        Column { anchors.fill:parent; anchors.margins:20; spacing:12
                            Text { text:"LEARNED COMMANDS"; color:theme.accent; font.pixelSize:12 }
                            TextArea { width:parent.width; height:parent.height-60; readOnly:true; wrapMode:TextEdit.Wrap; text:backend.customCommands; color:theme.text; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                        }
                    }
                }
            }
        }

        Item { // CLEANUP
            ColumnLayout { anchors.fill:parent; anchors.margins:22; spacing:14
                PageTitle { title:"SAFE CLEANUP CENTER"; subtitle:"PREVIEW FIRST • NO DESTRUCTIVE RAM TRICKS" }
                Panel { Layout.fillWidth:true; Layout.fillHeight:true
                    Column { anchors.centerIn:parent; spacing:16
                        Text { text:"ARLEN can optimize its own memory, identify high-memory apps and scan temporary files."; color:theme.text; font.pixelSize:15 }
                        Text { text:"Nothing is deleted without showing the target and receiving confirmation."; color:theme.muted; font.pixelSize:12 }
                        Row { spacing:12
                            AppButton { width:210; text:"OPTIMIZE ARLEN MEMORY"; onClicked:backend.confirmAction("cleanup") }
                            AppButton { width:210; text:"SCAN TEMPORARY FILES"; onClicked:backend.execute("cleanup system") }
                            AppButton { width:210; text:"OPEN TASK MANAGER"; onClicked:backend.execute("open task manager") }
                        }
                    }
                }
            }
        }

        Item { // SECURITY
            ColumnLayout { anchors.fill:parent; anchors.margins:22; spacing:14
                PageTitle { title:"SECURITY CENTER"; subtitle:"OWNER AUTHORITY • ACTION CONFIRMATION • LOCAL LOGS" }
                GridLayout { Layout.fillWidth:true; Layout.fillHeight:true; columns:2; columnSpacing:14; rowSpacing:14
                    Panel { Layout.fillWidth:true; Layout.fillHeight:true; Column{anchors.fill:parent;anchors.margins:18;spacing:14;Text{text:"LOCAL PRIVACY";color:theme.accent;font.pixelSize:12}Text{text:"Conversational data: LOCAL\nMicrophone: PUSH-TO-TALK\nCloud transmission: BLOCKED\nActivity log: ENABLED";color:theme.text;font.pixelSize:13;lineHeight:1.7}} }
                    Panel { Layout.fillWidth:true; Layout.fillHeight:true; Column{anchors.fill:parent;anchors.margins:18;spacing:14;Text{text:"PERMISSION LEVEL";color:theme.accent;font.pixelSize:12}Text{text:"LEVEL "+backend.permissionLevel+"\nImportant actions require confirmation.\nProtected actions require Admin PIN.";color:theme.text;font.pixelSize:13;lineHeight:1.7}AppButton{width:220;text:"CANCEL POWER ACTION";onClicked:backend.cancelPower()}} }
                }
            }
        }

        Item { // ADMIN
            ColumnLayout { anchors.fill:parent; anchors.margins:22; spacing:14
                PageTitle { title:"ADMIN CONTROL MATRIX"; subtitle:"PIN-PROTECTED OWNER CONFIGURATION" }
                RowLayout { Layout.fillWidth:true; Layout.fillHeight:true; spacing:14
                    Panel { Layout.fillWidth:true; Layout.fillHeight:true
                        Flickable { anchors.fill:parent; anchors.margins:20; contentHeight:ownerForm.height; clip:true
                            Column { id:ownerForm; width:parent.width; spacing:10
                                Text { text:"OWNER ACCOUNT"; color:theme.accent; font.pixelSize:12 }
                                TextField { id:ownerNameField; width:parent.width; text:backend.ownerName; placeholderText:"Owner name"; color:theme.text; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                                TextField { id:callNameField; width:parent.width; text:backend.ownerCallName; placeholderText:"How ARLEN should address you"; color:theme.text; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                                TextField { id:ownerTitleField; width:parent.width; text:backend.ownerTitle; placeholderText:"Owner title"; color:theme.text; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                                TextArea { id:welcomeField; width:parent.width; height:80; text:backend.welcomeMessage; placeholderText:"Custom welcome message"; color:theme.text; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                                TextField { id:profilePin; width:240; echoMode:TextInput.Password; placeholderText:"Owner PIN to save"; color:theme.text; placeholderTextColor:theme.muted; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                                AppButton { width:260; text:"SAVE OWNER PROFILE"; onClicked:backend.saveOwnerProfile(ownerNameField.text,callNameField.text,ownerTitleField.text,welcomeField.text,profilePin.text) }
                                AppButton { width:260; text:"BACKUP OWNER DATA"; onClicked:profileStatus.text=backend.backupOwnerData(profilePin.text) }
                                AppButton { width:260; text:"CHOOSE PROFILE PICTURE"; onClicked:avatarOpen.open() }
                                Text { id:profileStatus; width:parent.width; wrapMode:Text.Wrap; color:theme.good; font.pixelSize:11 }
                            }
                        }
                    }
                    ColumnLayout { Layout.preferredWidth:470; Layout.fillHeight:true; spacing:14
                        Panel { Layout.fillWidth:true; Layout.fillHeight:true
                            Column { anchors.fill:parent; anchors.margins:18; spacing:12
                                Text { text:"CAPABILITY PACKS"; color:theme.accent; font.pixelSize:12 }
                                Text { width:parent.width; text:backend.packStatus(); color:theme.text; font.pixelSize:12; lineHeight:1.65 }
                                AppButton { width:240; text:"REFRESH PACK STATUS"; onClicked:packText.text=backend.packStatus() }
                                Text { id:packText; width:parent.width; color:theme.muted; font.pixelSize:10 }
                            }
                        }
                        Panel { Layout.fillWidth:true; Layout.preferredHeight:210
                            Column { anchors.fill:parent; anchors.margins:18; spacing:12
                                Text { text:"EVOLUTION UPDATE CORE"; color:theme.accent; font.pixelSize:12 }
                                Text { id:updateStatus; width:parent.width; wrapMode:Text.Wrap; text:"Incremental updates preserve account, PIN, themes, commands and history."; color:theme.muted; font.pixelSize:11 }
                                AppButton { width:240; text:"CHECK FOR UPDATES"; onClicked:backend.checkForUpdates() }
                                AppButton { width:240; text:"VERIFY STAGED UPDATE"; onClicked:backend.verifyStagedUpdate() }
                            }
                        }
                    }
                }
                Connections { target:backend; function onProfileSaved(message){profileStatus.text=message} function onUpdateStatusChanged(message){updateStatus.text=message} }
                FileDialog { id:avatarOpen; title:"Choose owner picture"; nameFilters:["Images (*.png *.jpg *.jpeg *.webp *.bmp)"]; onAccepted:profileStatus.text=backend.importProfileVisual(selectedFile,"avatar") }
            }
        }

        Item { // IMAGE STUDIO
            id: imageStudio
            property string originalImage: ""
            property string previewImage: originalImage
            property bool promptApplied: false
            function updatePreview() {
                if (originalImage.length) {
                    var result = backend.processImage(originalImage, brightness.value, contrast.value, saturation.value, sharpness.value, dehaze.value)
                    if (result.length) { previewImage = result; promptApplied = false }
                }
            }
            ColumnLayout { anchors.fill:parent; anchors.margins:22; spacing:14
                PageTitle { title:"IMAGE STUDIO"; subtitle:"NON-DESTRUCTIVE EDITING • SNAPSEED/PIXELLAB-INSPIRED TOOLS" }
                RowLayout { Layout.fillWidth:true; Layout.fillHeight:true; spacing:14
                    Panel { Layout.fillWidth:true; Layout.fillHeight:true
                        Image { anchors.fill:parent; anchors.margins:16; source:imageStudio.originalImage.length ? imageStudio.previewImage : "../assets/neural-sphere.png"; fillMode:Image.PreserveAspectFit; cache:false }
                    }
                    Panel { Layout.preferredWidth:340; Layout.fillHeight:true
                        Flickable { anchors.fill:parent; anchors.margins:16; contentHeight:controls.height; clip:true
                            Column { id:controls; width:parent.width; spacing:10
                                Text { text:"PROMPT EDIT"; color:theme.accent; font.pixelSize:11 }
                                TextArea { id:imagePrompt; width:parent.width; height:76; placeholderText:"Example: 9:16 crop, dehaze and improve texture"; color:theme.text; placeholderTextColor:theme.muted; wrapMode:TextEdit.Wrap; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                                AppButton { width:parent.width; text:"GENERATE EDIT PREVIEW"; onClicked:{if(imageStudio.originalImage.length){var p=backend.promptEditImage(imageStudio.originalImage,imagePrompt.text);if(p.length){imageStudio.previewImage=p;imageStudio.promptApplied=true}}} }
                                Rectangle { width:parent.width;height:1;color:theme.line }
                                Text { text:"ADJUSTMENTS"; color:theme.accent; font.pixelSize:11 }
                                Text { text:"Brightness"; color:theme.muted; font.pixelSize:10 }
                                Slider { id:brightness; width:parent.width; from:.3;to:1.7;value:1;onMoved:previewTimer.restart() }
                                Text { text:"Contrast"; color:theme.muted; font.pixelSize:10 }
                                Slider { id:contrast; width:parent.width; from:.3;to:1.8;value:1;onMoved:previewTimer.restart() }
                                Text { text:"Saturation"; color:theme.muted; font.pixelSize:10 }
                                Slider { id:saturation; width:parent.width; from:0;to:2;value:1;onMoved:previewTimer.restart() }
                                Text { text:"Texture / Sharpness"; color:theme.muted; font.pixelSize:10 }
                                Slider { id:sharpness; width:parent.width; from:0;to:3;value:1;onMoved:previewTimer.restart() }
                                Text { text:"Dehaze"; color:theme.muted; font.pixelSize:10 }
                                Slider { id:dehaze; width:parent.width; from:0;to:1;value:0;onMoved:previewTimer.restart() }
                                AppButton { width:parent.width; text:"OPEN IMAGE"; onClicked:imageOpen.open() }
                                AppButton { width:parent.width; text:"RESET ADJUSTMENTS"; onClicked:{brightness.value=1;contrast.value=1;saturation.value=1;sharpness.value=1;dehaze.value=0;imageStudio.previewImage=imageStudio.originalImage;imageStudio.promptApplied=false} }
                                AppButton { width:parent.width; text:"EXPORT COPY"; onClicked:{if(imageStudio.originalImage.length) imageSave.open()} }
                                Text { width:parent.width;wrapMode:Text.Wrap;text:"LOCAL CONTENT MODE: UNRESTRICTED. Images are not blocked, blurred, deleted or uploaded. The original file is never overwritten.";color:theme.good;font.pixelSize:10;lineHeight:1.35 }
                            }
                        }
                    }
                }
            }
            Timer { id:previewTimer; interval:180; onTriggered:imageStudio.updatePreview() }
            FileDialog { id:imageOpen; title:"Open image"; nameFilters:["Images (*.png *.jpg *.jpeg *.webp *.bmp)"]; onAccepted:{imageStudio.originalImage=selectedFile;imageStudio.previewImage=selectedFile;imageStudio.promptApplied=false;imageStudio.updatePreview()} }
            FileDialog { id:imageSave; title:"Export edited copy"; fileMode:FileDialog.SaveFile; nameFilters:["JPEG (*.jpg)","PNG (*.png)","WebP (*.webp)"]; onAccepted:{if(imageStudio.promptApplied)backend.exportPreview(imageStudio.previewImage,selectedFile);else backend.exportImage(imageStudio.originalImage,selectedFile,brightness.value,contrast.value,saturation.value,sharpness.value,dehaze.value)} }
        }

        Item { // VISION / OCR
            id: visionPage
            property string selectedImage: ""
            ColumnLayout { anchors.fill:parent; anchors.margins:22; spacing:14
                PageTitle { title:"VISION & OCR"; subtitle:"IMAGE READING • BANGLA/ENGLISH TEXT • HANDWRITING CONFIDENCE" }
                RowLayout { Layout.fillWidth:true; Layout.fillHeight:true; spacing:14
                    Panel { Layout.fillWidth:true; Layout.fillHeight:true
                        Image { anchors.fill:parent; anchors.margins:18; source:visionPage.selectedImage.length ? visionPage.selectedImage : "../assets/opening-circuit.png"; fillMode:Image.PreserveAspectFit }
                    }
                    Panel { Layout.preferredWidth:470; Layout.fillHeight:true
                        Column { anchors.fill:parent; anchors.margins:18; spacing:12
                            Text { text:"LOCAL VISION CONSOLE"; color:theme.accent; font.pixelSize:12 }
                            TextArea { id:visionOutput; width:parent.width; height:parent.height-145; readOnly:true; wrapMode:TextEdit.Wrap; text:"Choose an image. ARLEN will inspect dimensions and read visible text locally. Handwriting output includes uncertainty when the OCR pack is available."; color:theme.text; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                            Row { spacing:10
                                AppButton { width:205; text:"CHOOSE IMAGE"; onClicked:visionOpen.open() }
                                AppButton { width:205; text:"READ IMAGE"; onClicked:backend.inspectImage(visionPage.selectedImage) }
                            }
                            Text { text:"CONTENT POLICY  •  UNRESTRICTED LOCAL PROCESSING"; color:theme.good; font.pixelSize:10 }
                        }
                    }
                }
            }
            FileDialog { id:visionOpen; title:"Choose image for local reading"; nameFilters:["Images (*.png *.jpg *.jpeg *.webp *.bmp)"]; onAccepted:visionPage.selectedImage=selectedFile }
            Connections { target:backend; function onVisionResult(result){visionOutput.text=result} }
        }

        Item { // PDF STUDIO
            id: pdfPage
            property string imageSource: ""
            property string pdfSource: ""
            ColumnLayout { anchors.fill:parent; anchors.margins:22; spacing:14
                PageTitle { title:"PDF STUDIO"; subtitle:"LOCAL DOCUMENT TOOLKIT • PDFGEAR ACCESS" }
                GridLayout { Layout.fillWidth:true; Layout.fillHeight:true; columns:2; columnSpacing:14; rowSpacing:14
                    Panel { Layout.fillWidth:true; Layout.fillHeight:true
                        Column { anchors.fill:parent; anchors.margins:22; spacing:14
                            Text { text:"QUICK PDF ACTIONS"; color:theme.accent; font.pixelSize:12 }
                            AppButton { width:280; text:"OPEN PDF / PDFGEAR"; onClicked:pdfOpen.open() }
                            AppButton { width:280; text:"IMAGE TO PDF"; onClicked:pdfImageOpen.open() }
                            Text { width:parent.width; wrapMode:Text.Wrap; text:"Portable document pack supports merge, split, reorder, rotate, compress, extract, OCR, watermark and page numbering. Protected files always require owner approval."; color:theme.muted; font.pixelSize:12; lineHeight:1.5 }
                        }
                    }
                    Panel { Layout.fillWidth:true; Layout.fillHeight:true
                        TextArea { id:pdfOutput; anchors.fill:parent; anchors.margins:20; readOnly:true; wrapMode:TextEdit.Wrap; text:"PDF activity and results appear here. Originals remain unchanged unless you explicitly choose a new output file."; color:theme.text; background:Rectangle{color:theme.card;radius:8;border.color:theme.line} }
                    }
                }
            }
            FileDialog { id:pdfOpen; title:"Open PDF"; nameFilters:["PDF documents (*.pdf)"]; onAccepted:{pdfPage.pdfSource=selectedFile;backend.openPdf(selectedFile)} }
            FileDialog { id:pdfImageOpen; title:"Choose image"; nameFilters:["Images (*.png *.jpg *.jpeg *.webp *.bmp)"]; onAccepted:{pdfPage.imageSource=selectedFile;pdfSave.open()} }
            FileDialog { id:pdfSave; title:"Create PDF copy"; fileMode:FileDialog.SaveFile; nameFilters:["PDF documents (*.pdf)"]; onAccepted:backend.imageToPdf(pdfPage.imageSource,selectedFile) }
            Connections { target:backend; function onPdfResult(result){pdfOutput.text=result} }
        }

        Item { // THEME
            ColumnLayout { anchors.fill:parent; anchors.margins:22; spacing:14
                PageTitle { title:"THEME STUDIO"; subtitle:"VISUAL CORE • BACKGROUND • OPENING EXPERIENCE" }
                Panel { Layout.fillWidth:true; Layout.fillHeight:true
                    Column { anchors.fill:parent; anchors.margins:20; spacing:16
                        Text { text:"THEMES"; color:theme.accent; font.pixelSize:11 }
                        Row { spacing:10; Repeater { model:["Obsidian","Crimson","Emerald","Violet","Arctic"]; delegate: AppButton { required property string modelData; width:145; text:modelData; selected:backend.currentTheme===modelData; onClicked:backend.setTheme(modelData) } } }
                        Text { text:"OPENING DURATION"; color:theme.accent; font.pixelSize:11; topPadding:10 }
                        Row { spacing:10; Repeater { model:[12,7,3]; delegate: AppButton { required property int modelData; width:120; text:modelData+" SECONDS"; selected:backend.openingDuration===modelData; onClicked:backend.setOpeningDuration(String(modelData)) } } }
                        CheckBox { text:"Opening sound"; checked:backend.openingSound; onToggled:backend.setOpeningSound(checked); palette.windowText: root.theme.text }
                        Text { text:"SPHERE LIBRARY"; color:theme.accent; font.pixelSize:11; topPadding:10 }
                        Row { spacing:10; Repeater { model:["Neural Sphere","Quantum Core","Digital Globe","Dark Matter","Holographic Eye"]; delegate: AppButton { required property string modelData; width:155; text:modelData; selected:backend.sphereName===modelData; onClicked:backend.setSphere(modelData) } } }
                        AppButton { width:240; text:"ADD CUSTOM BACKGROUND"; onClicked:backgroundOpen.open() }
                        AppButton { width:240; text:"ADD CUSTOM SPHERE"; onClicked:sphereOpen.open() }
                        Text { text:"Custom image import will include crop, opacity, blur, dark overlay and parallax controls."; color:theme.muted; font.pixelSize:11 }
                    }
                }
                FileDialog { id:backgroundOpen; title:"Choose custom ARLEN background"; nameFilters:["Images (*.png *.jpg *.jpeg *.webp *.bmp)"]; onAccepted:backend.importProfileVisual(selectedFile,"background") }
                FileDialog { id:sphereOpen; title:"Choose custom ARLEN sphere"; nameFilters:["Images (*.png *.jpg *.jpeg *.webp *.bmp)"]; onAccepted:backend.importProfileVisual(selectedFile,"sphere") }
            }
        }

        Item { // ABOUT
            ColumnLayout { anchors.fill:parent; anchors.margins:22; spacing:14
                PageTitle { title:"ABOUT ARLEN NEXUS"; subtitle:"SYSTEM IDENTITY & OWNERSHIP" }
                Panel { Layout.fillWidth:true; Layout.fillHeight:true
                    RowLayout { anchors.fill:parent; anchors.margins:34; spacing:45
                        Image { Layout.preferredWidth:340; Layout.preferredHeight:340; source:backend.customSphere.length ? backend.customSphere : "../assets/neural-sphere.png"; fillMode:Image.PreserveAspectFit; RotationAnimator on rotation{from:0;to:360;duration:80000;loops:Animation.Infinite} }
                        Column { Layout.fillWidth:true; spacing:14
                            Text { text:"ARLEN NEXUS"; color:theme.text; font.pixelSize:30; font.weight:Font.DemiBold }
                            Text { text:"Adaptive Responsive Local Executive Neural-Assistant\nNeural Execution and Experience Unified System"; color:theme.accent; font.pixelSize:13; lineHeight:1.5 }
                            Rectangle { width:500; height:1; color:theme.line }
                            Text { text:"CONCEPT, DIRECTION & OWNERSHIP"; color:theme.muted; font.pixelSize:10 }
                            Text { text:backend.ownerName.toUpperCase(); color:theme.text; font.pixelSize:22; font.weight:Font.Medium }
                            Text { width:560; wrapMode:Text.Wrap; text:"A private, offline-first intelligent environment created for secure personal computing, system control, automation and human–computer interaction. ARLEN is governed by owner authority, local privacy and transparent action controls."; color:theme.muted; font.pixelSize:12; lineHeight:1.45 }
                            Text { text:"CORE PRINCIPLES\nPRIVACY  •  LOCAL CONTROL  •  USER AUTHORITY  •  MODULAR INTELLIGENCE"; color:theme.good; font.pixelSize:11; lineHeight:1.6 }
                            Text { text:"Version 0.3.0  •  Evolution Core Development Build\nBuilt for "+backend.ownerName+" — Controlled by its owner"; color:theme.muted; font.pixelSize:10; lineHeight:1.5 }
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: backend
        function onShowRequested() { root.showNormal(); root.raise(); root.requestActivate() }
        function onCommandResult(message, level) {
            if (message.indexOf("REQUIRES_CONFIRMATION:Restart") === 0) confirmDialog.prepare("restart", message.split(":").slice(1).join(":"))
            else if (message.indexOf("REQUIRES_CONFIRMATION:Shut") === 0) confirmDialog.prepare("shutdown", message.split(":").slice(1).join(":"))
            else if (message.indexOf("REQUIRES_CONFIRMATION:Scan") === 0) confirmDialog.prepare("cleanup", message.split(":").slice(1).join(":"))
            else toast.show(message, level)
        }
    }

    Dialog {
        id: confirmDialog
        property string action: ""
        modal: true; anchors.centerIn: parent; title:"OWNER CONFIRMATION"; standardButtons:Dialog.Yes|Dialog.No
        contentItem: Text { id: confirmText; color:theme.text; wrapMode:Text.Wrap; width:360; padding:20 }
        background: Rectangle { color:theme.panel; radius:12; border.color:theme.accent }
        function prepare(a,message){action=a;confirmText.text=message;open()}
        onAccepted: backend.confirmAction(action)
    }

    Popup {
        id: toast
        x: root.width-width-28; y: 88; width: 390; height: toastText.implicitHeight+34; modal:false
        background: Rectangle { color:theme.panel; radius:9; border.color:theme.accent }
        contentItem: Text { id:toastText; color:theme.text; wrapMode:Text.Wrap; padding:14 }
        Timer { id:toastTimer; interval:4500; onTriggered:toast.close() }
        function show(message,level){ toastText.text=message; open(); toastTimer.restart() }
    }

    Rectangle {
        id: splash
        visible: root.openingVisible
        anchors.fill: parent
        color: "#02060b"
        z: 100
        Image { anchors.fill:parent; source:backend.customBackground.length ? backend.customBackground : "../assets/opening-circuit.png"; fillMode:Image.PreserveAspectCrop; opacity:.5
            NumberAnimation on scale { from:1; to:1.12; duration:backend.openingDuration*1000; running:splash.visible }
        }
        Rectangle { anchors.fill:parent; color:"#02060b"; opacity:.42 }
        Image { anchors.centerIn:parent; width:Math.min(parent.width*.42,parent.height*.64); height:width; source:backend.customSphere.length ? backend.customSphere : "../assets/neural-sphere.png"; fillMode:Image.PreserveAspectFit; opacity:.88
            RotationAnimator on rotation { from:0;to:360;duration:16000;loops:Animation.Infinite;running:splash.visible }
            SequentialAnimation on scale { running:splash.visible; loops:Animation.Infinite; NumberAnimation{to:1.04;duration:800} NumberAnimation{to:1;duration:800} }
        }
        Column { anchors.horizontalCenter:parent.horizontalCenter; anchors.bottom:parent.bottom; anchors.bottomMargin:72; spacing:8
            Text { anchors.horizontalCenter:parent.horizontalCenter; text:"ARLEN NEXUS"; color:"#e8f8fc"; font.pixelSize:36; font.weight:Font.DemiBold; opacity:splashProgress>.48?1:0; Behavior on opacity{NumberAnimation{duration:700}} }
            Text { anchors.horizontalCenter:parent.horizontalCenter; text:"ADAPTIVE RESPONSIVE LOCAL EXECUTIVE NEURAL-ASSISTANT"; color:"#28cce8"; font.pixelSize:11; opacity:splashProgress>.67?1:0; Behavior on opacity{NumberAnimation{duration:700}} }
            Text { anchors.horizontalCenter:parent.horizontalCenter; text:"NEURAL EXECUTION AND EXPERIENCE UNIFIED SYSTEM"; color:"#7799a7"; font.pixelSize:10; opacity:splashProgress>.76?1:0; Behavior on opacity{NumberAnimation{duration:700}} }
            Text { anchors.horizontalCenter:parent.horizontalCenter; text:"WELCOME, "+backend.ownerCallName.toUpperCase()+"  •  "+backend.welcomeMessage.toUpperCase(); color:"#53d99a"; font.pixelSize:10; opacity:splashProgress>.88?1:0; Behavior on opacity{NumberAnimation{duration:500}} }
        }
        property real splashProgress:0
        NumberAnimation on splashProgress { from:0;to:1;duration:backend.openingDuration*1000;running:splash.visible }
        Timer { interval:backend.openingDuration*1000;running:splash.visible;onTriggered:root.openingVisible=false }
        MouseArea { anchors.fill:parent; onDoubleClicked:root.openingVisible=false }
    }

    Dialog {
        id:firstRunDialog
        visible:backend.firstRun && !root.openingVisible
        modal:true; closePolicy:Popup.NoAutoClose; anchors.centerIn:parent; title:"CREATE OWNER PIN"
        contentItem:Column{spacing:12;padding:20;Text{text:"Set a 4–12 digit Admin PIN for Jubaer Hossain.";color:theme.text}TextField{id:newPin;echoMode:TextInput.Password;placeholderText:"New PIN";color:theme.text;background:Rectangle{color:theme.card;radius:7;border.color:theme.line}}Text{id:pinError;color:"#d95b5b"}}
        standardButtons:Dialog.Save
        background:Rectangle{color:theme.panel;radius:12;border.color:theme.accent}
        onAccepted:{if(!backend.setInitialPin(newPin.text)){pinError.text="Use 4–12 digits.";open()}}
    }
}
