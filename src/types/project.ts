/**
 * Tutora AI Project Schema & Public Types
 */

export type AspectRatio = "16:9" | "9:16" | "1:1" | "4:3" | "custom";

export type KeynoteLayout = "right" | "left" | "top" | "bottom" | "fullscreen";

export type KeynoteDurationPreset = "fast" | "standard" | "cinematic";

export interface ZoomKeyframe {
  id: string;
  start: number;
  end: number;
  scale: number;
  targetX: number;
  targetY: number;
  easing?: "tutora" | "smooth" | "glide" | "snappy" | "linear";
}

export interface CursorSettings {
  scale: number;
  style: "default" | "windows11" | "macos" | "minimal";
  springPhysics: boolean;
  clickShockwave: boolean;
  bounceMultiplier: number;
}

export interface WebcamOverlayConfig {
  enabled: boolean;
  reactsToZoom: boolean;
  mirror: boolean;
  position: "top-left" | "top-right" | "bottom-left" | "bottom-right";
  sizePercent: number;
  borderRadius?: number;
}

export interface VoiceoverSegment {
  id: string;
  start: number;
  duration?: number;
  text: string;
  voiceName?: string;
}

export interface TutoraProjectManifest {
  version: string;
  appName: "Tutora AI";
  project: {
    id: string;
    name: string;
    createdAt: number;
    updatedAt: number;
    canvas: {
      aspectRatio: AspectRatio;
      width: number;
      height: number;
      padding: number;
      borderRadius: number;
    };
    timeline: {
      durationSeconds: number;
      zoomKeyframes: ZoomKeyframe[];
      cursor: CursorSettings;
      webcam: WebcamOverlayConfig;
      voiceover: {
        engine: "kokoro-neural-offline";
        voice: string;
        segments: VoiceoverSegment[];
      };
    };
  };
}
