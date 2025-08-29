import React, { useState, useEffect } from 'react';

const CrankSliderDemo = () => {
  const [crankAngle, setCrankAngle] = useState(0);
  const [crankLength, setCrankLength] = useState(40);
  const [rodLength, setRodLength] = useState(120);
  const [isAnimating, setIsAnimating] = useState(false);
  
  // Canvas dimensions and origin
  const width = 500;
  const height = 200;
  const originX = 100;
  const originY = height / 2;
  
  // Calculate positions
  const crankEndX = originX + crankLength * Math.cos(crankAngle * Math.PI / 180);
  const crankEndY = originY + crankLength * Math.sin(crankAngle * Math.PI / 180);
  
  // Calculate slider position using slider-crank equation
  const sliderX = originX + crankLength * Math.cos(crankAngle * Math.PI / 180) + 
                 rodLength * Math.sqrt(1 - Math.pow((crankLength * Math.sin(crankAngle * Math.PI / 180) / rodLength), 2));
  const sliderY = originY;
  
  // Calculate connecting rod angle
  const rodAngle = Math.atan2(sliderY - crankEndY, sliderX - crankEndX) * 180 / Math.PI;
  
  // Animation effect
  useEffect(() => {
    let animationId;
    
    if (isAnimating) {
      let lastTimestamp = 0;
      const step = (timestamp) => {
        if (!lastTimestamp) lastTimestamp = timestamp;
        const elapsed = timestamp - lastTimestamp;
        
        // Update angle at a rate of 90 degrees per second
        if (elapsed > 10) {  // Update every 10ms
          setCrankAngle((prevAngle) => (prevAngle + 1) % 360);
          lastTimestamp = timestamp;
        }
        
        animationId = requestAnimationFrame(step);
      };
      
      animationId = requestAnimationFrame(step);
    }
    
    return () => {
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
    };
  }, [isAnimating]);
  
  return (
    <div className="tw-flex tw-flex-col tw-items-center tw-p-4 tw-bg-white tw-rounded-lg tw-shadow">
      <h3 className="tw-text-xl tw-font-bold tw-mb-4">Slider-Crank Mechanism</h3>
      
      <div className="tw-mb-4 tw-w-full">
        <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} className="tw-border tw-border-gray-300 tw-bg-gray-50">
          {/* Fixed pivot */}
          <circle cx={originX} cy={originY} r={5} fill="#1F2937" />
          
          {/* Crank */}
          <line 
            x1={originX} 
            y1={originY} 
            x2={crankEndX} 
            y2={crankEndY} 
            stroke="#EF4444" 
            strokeWidth={4} 
          />
          
          {/* Connecting rod */}
          <line 
            x1={crankEndX} 
            y1={crankEndY} 
            x2={sliderX} 
            y2={sliderY} 
            stroke="#3B82F6" 
            strokeWidth={3} 
          />
          
          {/* Slider track */}
          <line 
            x1={originX - 20} 
            y1={originY} 
            x2={originX + crankLength + rodLength + 20} 
            y2={originY} 
            stroke="#9CA3AF" 
            strokeWidth={1} 
            strokeDasharray="4,4" 
          />
          
          {/* Slider block */}
          <rect 
            x={sliderX - 15} 
            y={sliderY - 15} 
            width={30} 
            height={30} 
            fill="#10B981" 
            stroke="#065F46" 
            strokeWidth={1} 
          />
          
          {/* Joints */}
          <circle cx={crankEndX} cy={crankEndY} r={4} fill="#6366F1" />
          
          {/* Labels */}
          <text x={originX - 20} y={originY - 15} className="tw-text-sm" fill="#1F2937">O</text>
          <text x={crankEndX + 5} y={crankEndY - 5} className="tw-text-sm" fill="#1F2937">B</text>
          <text x={sliderX - 5} y={sliderY - 20} className="tw-text-sm" fill="#1F2937">P</text>
          
          {/* Measurements */}
          <text x={originX + crankLength/2 - 20} y={originY - 15} className="tw-text-xs" fill="#EF4444">r = {crankLength}mm</text>
          <text x={crankEndX + rodLength/2 - 20} y={crankEndY - 20} className="tw-text-xs" fill="#3B82F6">l = {rodLength}mm</text>
          <text x={originX + 10} y={originY + 25} className="tw-text-xs" fill="#1F2937">{Math.round(sliderX - originX)}mm</text>
        </svg>
      </div>
      
      <div className="tw-w-full tw-flex tw-flex-col md:tw-flex-row md:tw-justify-between tw-gap-4">
        <div className="tw-flex tw-flex-col tw-gap-2 tw-w-full md:tw-w-1/3">
          <label className="tw-font-medium tw-text-gray-700">Crank Angle: {crankAngle}°</label>
          <input 
            type="range" 
            min="0" 
            max="359" 
            value={crankAngle} 
            onChange={(e) => setCrankAngle(parseInt(e.target.value))}
            disabled={isAnimating}
            className="tw-w-full"
          />
        </div>
        
        <div className="tw-flex tw-flex-col tw-gap-2 tw-w-full md:tw-w-1/3">
          <label className="tw-font-medium tw-text-gray-700">Crank Length: {crankLength}mm</label>
          <input 
            type="range" 
            min="20" 
            max="80" 
            value={crankLength} 
            onChange={(e) => setCrankLength(parseInt(e.target.value))}
            className="tw-w-full"
          />
        </div>
        
        <div className="tw-flex tw-flex-col tw-gap-2 tw-w-full md:tw-w-1/3">
          <label className="tw-font-medium tw-text-gray-700">Rod Length: {rodLength}mm</label>
          <input 
            type="range" 
            min="80" 
            max="200" 
            value={rodLength} 
            onChange={(e) => setRodLength(parseInt(e.target.value))}
            className="tw-w-full"
          />
        </div>
      </div>
      
      <div className="tw-mt-4">
        <button 
          onClick={() => setIsAnimating(!isAnimating)}
          className="tw-px-4 tw-py-2 tw-bg-blue-600 tw-text-white tw-rounded hover:tw-bg-blue-700 tw-transition"
        >
          {isAnimating ? 'Pause' : 'Animate'}
        </button>
      </div>
      
      <div className="tw-mt-4 tw-text-gray-700">
        <p className="tw-text-sm">
          <strong>Slider Position:</strong> {Math.round(sliderX - originX)}mm from the origin
        </p>
        <p className="tw-text-sm">
          <strong>Rod Angle:</strong> {Math.round(rodAngle)}° with the horizontal
        </p>
      </div>
    </div>
  );
};

export default CrankSliderDemo;
