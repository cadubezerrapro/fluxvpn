#import <Cocoa/Cocoa.h>
#import <WebKit/WebKit.h>

@interface AppDelegate : NSObject <NSApplicationDelegate, NSWindowDelegate, WKNavigationDelegate>
@property (strong, nonatomic) NSWindow *window;
@property (strong, nonatomic) WKWebView *webView;
@end

@implementation AppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
    // 1. Inicia o motor de background Python (flux_engine.py)
    NSString *bundlePath = [[NSBundle mainBundle] bundlePath];
    NSString *enginePath = [bundlePath stringByAppendingPathComponent:@"Contents/Resources/core/flux_engine.py"];
    if ([[NSFileManager defaultManager] fileExistsAtPath:enginePath]) {
        NSString *bgCmd = [NSString stringWithFormat:@"pgrep -f flux_engine.py >/dev/null 2>&1 || (python3 \"%@\" >/dev/null 2>&1 &)", enginePath];
        system([bgCmd UTF8String]);
    }

    // 2. Cria o Menu Bar Nativo Apple (FLUX VPN)
    NSMenu *menubar = [[NSMenu alloc] init];
    NSMenuItem *appMenuItem = [[NSMenuItem alloc] init];
    [menubar addItem:appMenuItem];
    [NSApp setMainMenu:menubar];

    NSMenu *appMenu = [[NSMenu alloc] init];
    NSString *appName = @"FLUX VPN";
    NSMenuItem *aboutItem = [[NSMenuItem alloc] initWithTitle:[NSString stringWithFormat:@"Sobre o %@", appName]
                                                       action:@selector(orderFrontStandardAboutPanel:)
                                                keyEquivalent:@""];
    [appMenu addItem:aboutItem];
    [appMenu addItem:[NSMenuItem separatorItem]];
    NSMenuItem *hideItem = [[NSMenuItem alloc] initWithTitle:[NSString stringWithFormat:@"Ocultar %@", appName]
                                                      action:@selector(hide:)
                                               keyEquivalent:@"h"];
    [appMenu addItem:hideItem];
    NSMenuItem *hideOthersItem = [[NSMenuItem alloc] initWithTitle:@"Ocultar Outros"
                                                            action:@selector(hideOtherApplications:)
                                                     keyEquivalent:@"h"];
    [hideOthersItem setKeyEquivalentModifierMask:(NSEventModifierFlagOption | NSEventModifierFlagCommand)];
    [appMenu addItem:hideOthersItem];
    [appMenu addItem:[NSMenuItem separatorItem]];
    NSMenuItem *quitItem = [[NSMenuItem alloc] initWithTitle:[NSString stringWithFormat:@"Encerrar %@", appName]
                                                      action:@selector(terminate:)
                                               keyEquivalent:@"q"];
    [appMenu addItem:quitItem];
    [appMenuItem setSubmenu:appMenu];

    // 3. Janela Nativa macOS Apple Style
    NSRect frame = NSMakeRect(0, 0, 1080, 720);
    NSUInteger style = NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable;
    self.window = [[NSWindow alloc] initWithContentRect:frame
                                              styleMask:style
                                                backing:NSBackingStoreBuffered
                                                  defer:NO];
    self.window.title = @"FLUX VPN";
    self.window.titleVisibility = NSWindowTitleHidden;
    self.window.titlebarAppearsTransparent = YES;
    self.window.styleMask |= NSWindowStyleMaskFullSizeContentView;
    [self.window center];
    self.window.delegate = self;

    // 4. Configura WebKit Nativo
    WKWebViewConfiguration *config = [[WKWebViewConfiguration alloc] init];
    [config.preferences setValue:@YES forKey:@"allowFileAccessFromFileURLs"];
    [config.preferences setValue:@YES forKey:@"developerExtrasEnabled"];
    
    self.webView = [[WKWebView alloc] initWithFrame:self.window.contentView.bounds configuration:config];
    self.webView.autoresizingMask = NSViewWidthSizable | NSViewHeightSizable;
    self.webView.navigationDelegate = self;
    @try {
        [self.webView setValue:@NO forKey:@"drawsBackground"]; // Fundo transparente moderno
    } @catch (NSException *e) {}
    [self.window.contentView addSubview:self.webView];

    // 5. Carrega o index.html nativo do bundle
    NSString *resourcesPath = [bundlePath stringByAppendingPathComponent:@"Contents/Resources"];
    NSString *indexPath = [resourcesPath stringByAppendingPathComponent:@"index.html"];
    
    // Fallback para desenvolvimento caso rode fora do bundle
    if (![[NSFileManager defaultManager] fileExistsAtPath:indexPath]) {
        NSString *cwd = [[NSFileManager defaultManager] currentDirectoryPath];
        indexPath = [cwd stringByAppendingPathComponent:@"index.html"];
        resourcesPath = cwd;
    }

    NSURL *fileURL = [NSURL fileURLWithPath:indexPath];
    NSURL *readAccessURL = [NSURL fileURLWithPath:resourcesPath];
    [self.webView loadFileURL:fileURL allowingReadAccessToURL:readAccessURL];

    [self.window makeKeyAndOrderFront:nil];
    [NSApp activateIgnoringOtherApps:YES];
}

- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *)sender {
    return YES;
}

- (void)applicationWillTerminate:(NSNotification *)aNotification {
    // Restaura configurações normais de rede e encerra o motor Python
    system("pkill -f flux_engine.py >/dev/null 2>&1");
    system("networksetup -setsocksfirewallproxystate Wi-Fi off >/dev/null 2>&1");
}

@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSApplication *app = [NSApplication sharedApplication];
        AppDelegate *delegate = [[AppDelegate alloc] init];
        app.delegate = delegate;
        [app setActivationPolicy:NSApplicationActivationPolicyRegular];
        [app run];
    }
    return 0;
}
